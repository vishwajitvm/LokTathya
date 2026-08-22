import pytest
import uuid
from ingestion.tasks import source_discovery, fetch_task, parse_pdf, parse_tabular
from models.source import Source, SourceEndpoint
from sqlalchemy.orm import Session
from core.database import SessionLocal

@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_parse_pdf_task():
    res = parse_pdf.apply(args=["raw/some_doc.pdf"])
    assert res.result["status"] == "SUCCESS"
    assert res.result["parser"] == "PDF"

def test_parse_tabular_task():
    res = parse_tabular.apply(args=["raw/sheet.xlsx"])
    assert res.result["status"] == "SUCCESS"
    assert res.result["parser"] == "TABULAR"

def test_source_discovery_task(db_session: Session):
    source = Source(name="Discovery Task Source", official_domain="completion.gov.in", status="ACTIVE")
    db_session.add(source)
    db_session.commit()

    res = source_discovery.apply(args=[str(source.id)])
    # Since completion.gov.in has no sitemap, discovered count should be 0 or return success
    assert res.result["status"] == "SUCCESS"
