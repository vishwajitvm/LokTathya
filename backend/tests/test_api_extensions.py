import pytest
import uuid
from fastapi.testclient import TestClient
from main import app
from core.database import SessionLocal
from models.source import Source, SourceEndpoint, Quarantine, IngestionRun

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def test_discovery_run_endpoint(db):
    source = Source(name="API Discovery Test Source", status="ACTIVE")
    db.add(source)
    db.commit()
    
    response = client.post(f"/api/v1/discovery/run?source_id={source.id}&max_pages=20")
    assert response.status_code == 200
    data = response.json()
    assert data["source_id"] == str(source.id)
    assert data["status"] == "RUNNING"
    assert data["max_pages"] == 20

def test_discovery_run_status(db):
    source = Source(name="API Run Status Source", status="ACTIVE")
    db.add(source)
    db.commit()
    
    # Trigger run via API
    res_run = client.post(f"/api/v1/discovery/run?source_id={source.id}&max_pages=20")
    run_id = res_run.json()["run_id"]
    
    response = client.get(f"/api/v1/discovery/runs/{run_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["run_id"] == run_id
    assert data["status"] == "RUNNING"

def test_discovery_candidates(db):
    source = Source(name="API Candidates Source", status="ACTIVE")
    db.add(source)
    db.commit()
    
    candidate = SourceEndpoint(
        source_id=source.id,
        url="https://completion.gov.in/discovered-candidate.pdf",
        method="GET",
        status="CANDIDATE",
        expected_format="PDF"
    )
    db.add(candidate)
    db.commit()
    
    response = client.get("/api/v1/discovery/candidates")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(d["url"] == candidate.url for d in data)

def test_quarantine_endpoints(db):
    source = Source(name="API Quarantine Source", status="ACTIVE")
    db.add(source)
    db.commit()
    
    item = Quarantine(
        source_id=source.id,
        artifact_path="raw/malformed.pdf",
        error_type="PDFParserError",
        message="EOF marker not found",
        stack_trace="Traceback: ...",
        status="QUARANTINED"
    )
    db.add(item)
    db.commit()
    
    # List quarantine
    response = client.get("/api/v1/quarantine")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    
    quarantine_id = str(item.id)
    
    # Detail quarantine
    response_detail = client.get(f"/api/v1/quarantine/{quarantine_id}")
    assert response_detail.status_code == 200
    assert response_detail.json()["id"] == quarantine_id
    
    # Retry item
    response_retry = client.post(f"/api/v1/quarantine/{quarantine_id}/retry")
    assert response_retry.status_code == 200
    assert response_retry.json()["status"] == "RETRY_PENDING"
    
    # Resolve item
    response_resolve = client.post(f"/api/v1/quarantine/{quarantine_id}/resolve")
    assert response_resolve.status_code == 200
    assert response_resolve.json()["status"] == "RESOLVED"
