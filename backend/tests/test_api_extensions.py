import pytest
import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_discovery_run_endpoint():
    source_id = str(uuid.uuid4())
    response = client.post(f"/api/v1/discovery/run?source_id={source_id}&max_pages=20")
    assert response.status_code == 200
    data = response.json()
    assert data["source_id"] == source_id
    assert data["status"] == "RUNNING"
    assert data["max_pages"] == 20

def test_discovery_run_status():
    run_id = str(uuid.uuid4())
    response = client.get(f"/api/v1/discovery/runs/{run_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["run_id"] == run_id
    assert data["status"] == "COMPLETED"

def test_discovery_candidates():
    response = client.get("/api/v1/discovery/candidates")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["type"] in ["PDF", "HTML"]

def test_quarantine_endpoints():
    # List quarantine
    response = client.get("/api/v1/quarantine")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    
    quarantine_id = data[0]["id"]
    
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
