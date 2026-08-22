import pytest
import io
import uuid
import json
import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from core.database import SessionLocal
from core.http_client import ResilientHTTPClient
from core.url_utils import URLCanonicalizer
from storage.minio_client import MinIOStorageService
from ingestion.parser_factory import ParserFactory
from ingestion.batch import IngestionBatchManager
from models.source import Source, SourceEndpoint, FetchEvent, Document, ContentVersion
from models.web_page import WebPage, WebPageVersion
from models.observation import Observation
from models.provenance import Claim, Evidence, CanonicalFact

@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_ssrf_and_redirect_ssrf():
    client = ResilientHTTPClient()
    # Unsafe local address
    res = asyncio.run(client.fetch("http://127.0.0.1:8000/"))
    assert res["status"] == "BLOCKED"
    
    # Metadata endpoint
    res2 = asyncio.run(client.fetch("http://169.254.169.254/latest/meta-data/"))
    assert res2["status"] == "BLOCKED"

def test_minio_and_provenance_flow(db_session: Session):
    # Setup test source
    source = Source(
        name="Test Ingestion Authority",
        authority_name="Test Authority",
        category="budget",
        status="ACTIVE"
    )
    db_session.add(source)
    db_session.commit()
    
    endpoint = SourceEndpoint(
        source_id=source.id,
        url="https://example.gov.in/test-budget.html",
        method="GET",
        status="ACTIVE"
    )
    db_session.add(endpoint)
    db_session.commit()

    # 1. Simulate HTML Ingestion
    html_content = b"<html><head><title>Factual Budget</title></head><body><p>Allocation: 50 crore</p></body></html>"
    content_hash = "mock_html_hash_1"
    
    # Put to MinIO
    storage = MinIOStorageService()
    storage_path = f"raw/endpoint_{endpoint.id}/{content_hash}"
    assert storage.put(storage_path, html_content, content_type="text/html")
    
    # Create WebPage representation
    web_page = WebPage(
        source_id=source.id,
        endpoint_id=endpoint.id,
        canonical_url=URLCanonicalizer.canonicalize(endpoint.url),
        current_url=endpoint.url,
        title="Factual Budget",
        page_type="BUDGET"
    )
    db_session.add(web_page)
    db_session.commit()
    
    # Parse HTML
    meta = {
        "document_id": str(web_page.id),
        "source_id": str(source.id),
        "storage_path": storage_path,
        "base_url": endpoint.url
    }
    parser = ParserFactory.get_parser("HTML")
    parsed_res = parser.parse(html_content, meta)
    
    assert parsed_res["status"] == "SUCCESS"
    assert "Allocation: 50 crore" in parsed_res["text_content"]
    
    # Store WebPageVersion
    version = WebPageVersion(
        page_id=web_page.id,
        version_number=1,
        content_hash=content_hash,
        raw_html_hash=content_hash,
        storage_path=storage_path,
        normalized_path=f"normalized/{content_hash}.txt",
        extracted_metadata={"title": "Factual Budget"}
    )
    db_session.add(version)
    db_session.commit()
    
    # 2. Observation creation
    observation = Observation(
        source_id=source.id,
        web_page_id=web_page.id,
        web_page_version_id=version.id,
        entity_type="budget_allocation",
        field_name="allocation",
        raw_value="50 crore",
        normalized_value={"amount": 500000000, "unit": "INR"},
        status="VALIDATED"
    )
    db_session.add(observation)
    db_session.commit()
    
    # 3. Provenance creation (CanonicalFact -> Claim -> Evidence)
    canonical = CanonicalFact(
        entity_id="budget-MH-2026",
        attribute_name="allocation",
        value={"amount": 500000000, "unit": "INR"},
        status="CURRENT",
        conflict_status="CONSISTENT"
    )
    db_session.add(canonical)
    db_session.commit()
    
    claim = Claim(
        claim_level="RECORD",
        description="Budget Allocation parsed from MH budget portal",
        canonical_fact_id=canonical.id,
        status="CURRENT"
    )
    db_session.add(claim)
    db_session.commit()
    
    evidence = Evidence(
        claim_id=claim.id,
        source_id=source.id,
        endpoint_id=endpoint.id,
        record_id=str(observation.id)
    )
    db_session.add(evidence)
    db_session.commit()
    
    # Verify DB state
    assert db_session.query(Observation).filter(Observation.id == observation.id).first() is not None
    assert db_session.query(Evidence).filter(Evidence.id == evidence.id).first() is not None
    
    # Cleanup
    storage.delete_if_allowed(storage_path)
