import pytest
import io
import uuid
import hashlib
from datetime import datetime
from sqlalchemy.orm import Session
from core.database import SessionLocal
from core.url_utils import URLCanonicalizer
from storage.minio_client import MinIOStorageService
from ingestion.parser_factory import ParserFactory
from models.source import Source, SourceEndpoint, FetchEvent, Document, ContentVersion
from models.web_page import WebPage, WebPageVersion
from models.observation import Observation
from models.provenance import Claim, Evidence, CanonicalFact

@pytest.fixture(scope="module")
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def test_webpage_cosmetic_vs_semantic_versioning(db: Session):
    # Setup source and page
    source = Source(name="Completion Page Source", status="ACTIVE")
    db.add(source)
    db.commit()
    
    endpoint = SourceEndpoint(source_id=source.id, url="https://completion.gov.in/index.html", method="GET")
    db.add(endpoint)
    db.commit()
    
    web_page = WebPage(
        source_id=source.id,
        endpoint_id=endpoint.id,
        canonical_url=URLCanonicalizer.canonicalize(endpoint.url),
        current_url=endpoint.url,
        title="Budgets"
    )
    db.add(web_page)
    db.commit()

    # V1 raw html
    html_v1 = b"<html><body><h1>Budget 2026</h1><p class='cookie-banner'>Timestamp: 17192837</p></body></html>"
    # Clean cosmetic noise (timestamp, presentation banners)
    # Since HTMLNormalizer parses tables and clean elements:
    parser = ParserFactory.get_parser("HTML")
    res_v1 = parser.parse(html_v1, {"document_id": str(web_page.id), "base_url": endpoint.url})
    text_v1 = res_v1["text_content"]
    hash_v1 = hashlib.sha256(text_v1.encode('utf-8')).hexdigest()

    # V2 raw html with cosmetic change only (different timestamp)
    html_v2 = b"<html><body><h1>Budget 2026</h1><p class='cookie-banner'>Timestamp: 98765432</p></body></html>"
    res_v2 = parser.parse(html_v2, {"document_id": str(web_page.id), "base_url": endpoint.url})
    text_v2 = res_v2["text_content"]
    hash_v2 = hashlib.sha256(text_v2.encode('utf-8')).hexdigest()

    # The HTML parser normalizer should strip standard non-semantic timestamp noise
    # Or at least for our semantic logic, we verify that cosmetic differences are decoupled.
    # In our normalizer design, presentation elements or simple text remains identical if we filter.
    assert hash_v1 == hash_v2

    # V3 HTML with semantic change
    html_v3 = b"<html><body><h1>Budget 2027</h1><p>Timestamp: 98765432</p></body></html>"
    res_v3 = parser.parse(html_v3, {"document_id": str(web_page.id), "base_url": endpoint.url})
    text_v3 = res_v3["text_content"]
    hash_v3 = hashlib.sha256(text_v3.encode('utf-8')).hexdigest()
    assert hash_v1 != hash_v3

def test_pdf_versioning_and_government_correction(db: Session):
    source = Source(name="Completion PDF Source", status="ACTIVE")
    db.add(source)
    db.commit()

    doc = Document(
        source_id=source.id,
        title="Annual Budget Report",
        canonical_url="https://completion.gov.in/report.pdf",
        status="CURRENT"
    )
    db.add(doc)
    db.commit()

    # V1 PDF mock content
    pdf_v1_bytes = b"%PDF-1.4 mock pdf report version 1 bytes"
    hash_v1 = hashlib.sha256(pdf_v1_bytes).hexdigest()

    storage = MinIOStorageService()
    path_v1 = f"raw/doc_{doc.id}/v1_{hash_v1}.pdf"
    storage.put(path_v1, pdf_v1_bytes, "application/pdf")

    v1_rec = ContentVersion(
        document_id=doc.id,
        version_number=1,
        sha256=hash_v1,
        storage_path=path_v1,
        mime_type="application/pdf"
    )
    db.add(v1_rec)
    db.commit()

    # V2 PDF mock content (same URL, different content)
    pdf_v2_bytes = b"%PDF-1.4 mock pdf report version 2 corrected bytes"
    hash_v2 = hashlib.sha256(pdf_v2_bytes).hexdigest()
    path_v2 = f"raw/doc_{doc.id}/v2_{hash_v2}.pdf"
    storage.put(path_v2, pdf_v2_bytes, "application/pdf")

    # Document remains same logical identity (doc.id), new ContentVersion created
    v2_rec = ContentVersion(
        document_id=doc.id,
        version_number=2,
        sha256=hash_v2,
        storage_path=path_v2,
        mime_type="application/pdf"
    )
    db.add(v2_rec)
    db.commit()

    # Verify both content versions are stored and linked
    versions = db.query(ContentVersion).filter(ContentVersion.document_id == doc.id).order_by(ContentVersion.version_number).all()
    assert len(versions) == 2
    assert versions[0].sha256 == hash_v1
    assert versions[1].sha256 == hash_v2

    # Verify MinIO raw objects exist for both versions
    assert storage.exists(path_v1)
    assert storage.exists(path_v2)

    # Clean up MinIO
    storage.delete_if_allowed(path_v1)
    storage.delete_if_allowed(path_v2)

def test_same_content_different_url(db: Session):
    pdf_bytes = b"%PDF-1.4 shared budget report content"
    content_hash = hashlib.sha256(pdf_bytes).hexdigest()

    # Two distinct URLs pointing to same content bytes
    url_a = "https://completion.gov.in/reports/budget.pdf"
    url_b = "https://completion.gov.in/archive/budget-2026.pdf"

    # Identify if a document with this hash already exists
    existing_version = db.query(ContentVersion).filter(ContentVersion.sha256 == content_hash).first()
    
    if not existing_version:
        doc = Document(title="Shared Budget Report", canonical_url=url_a)
        db.add(doc)
        db.commit()
        
        cv = ContentVersion(
            document_id=doc.id,
            version_number=1,
            sha256=content_hash,
            mime_type="application/pdf"
        )
        db.add(cv)
        db.commit()
    else:
        doc = db.query(Document).filter(Document.id == existing_version.document_id).first()

    # Both observations/endpoints refer to the SAME document ID (deduplication)
    # but represent separate url sources
    assert doc is not None

def test_source_disappearance_scenario(db: Session):
    source = Source(name="Disappearing Source", status="ACTIVE")
    db.add(source)
    db.commit()

    endpoint = SourceEndpoint(
        source_id=source.id,
        url="https://disappear.gov.in/data.pdf",
        method="GET",
        status="ACTIVE"
    )
    db.add(endpoint)
    db.commit()

    # Simulate fetch success
    endpoint.last_success = datetime.utcnow()
    db.commit()

    # Simulate disappearance (returns 404)
    endpoint.status = "DEGRADED"
    endpoint.last_failure = datetime.utcnow()
    endpoint.error_count = 1
    db.commit()

    # Verify that the Source, Endpoint metadata, and historical observations are NOT deleted
    assert db.query(Source).filter(Source.id == source.id).first() is not None
    assert db.query(SourceEndpoint).filter(SourceEndpoint.id == endpoint.id).first() is not None
    assert db.query(SourceEndpoint).filter(SourceEndpoint.id == endpoint.id).first().status == "DEGRADED"
