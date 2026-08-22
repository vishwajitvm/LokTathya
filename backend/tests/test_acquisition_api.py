import pytest
import uuid
from fastapi.testclient import TestClient
from main import app
from core.database import SessionLocal
from models.source import Source, SourceEndpoint, IngestionBatch, IngestionRun, Dataset

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    session = SessionLocal()
    # Keep track of IDs to delete
    source_ids = []
    endpoint_ids = []
    run_ids = []
    dataset_ids = []
    batch_ids = []
    try:
        yield (session, source_ids, endpoint_ids, run_ids, dataset_ids, batch_ids)
        # Teardown: delete strictly by ID in correct dependency order
        if batch_ids:
            session.query(IngestionBatch).filter(IngestionBatch.id.in_(batch_ids)).delete(synchronize_session=False)
        if run_ids:
            session.query(IngestionRun).filter(IngestionRun.id.in_(run_ids)).delete(synchronize_session=False)
        if dataset_ids:
            session.query(Dataset).filter(Dataset.id.in_(dataset_ids)).delete(synchronize_session=False)
        if endpoint_ids:
            session.query(SourceEndpoint).filter(SourceEndpoint.id.in_(endpoint_ids)).delete(synchronize_session=False)
        if source_ids:
            session.query(Source).filter(Source.id.in_(source_ids)).delete(synchronize_session=False)
        session.commit()
    finally:
        session.close()

def test_source_endpoints_modification_api(db):
    session, source_ids, endpoint_ids, run_ids, dataset_ids, batch_ids = db
    
    source = Source(name="Acquisition Ingest Test Source", status="ACTIVE")
    session.add(source)
    session.commit()
    source_ids.append(source.id)

    # Create endpoint via POST API
    res_ep = client.post(f"/api/v1/sources/{source.id}/endpoints?url=https://gov.in/feed.xml")
    assert res_ep.status_code == 200
    ep_id = res_ep.json()["endpoint_id"]
    endpoint_ids.append(uuid.UUID(ep_id))

    # Patch endpoint status
    res_patch = client.patch(f"/api/v1/sources/endpoints/{ep_id}", json={"status": "DISABLED"})
    assert res_patch.status_code == 200

def test_discovery_runs_and_candidates_api(db):
    session, source_ids, endpoint_ids, run_ids, dataset_ids, batch_ids = db
    
    source = Source(name="Discovery Candidate Test Source", status="ACTIVE")
    session.add(source)
    session.commit()
    source_ids.append(source.id)

    dataset = Dataset(source_id=source.id, name="Discovery Dataset")
    session.add(dataset)
    session.commit()
    dataset_ids.append(dataset.id)

    import datetime
    run = IngestionRun(dataset_id=dataset.id, started_at=datetime.datetime.utcnow(), status="RUNNING")
    session.add(run)
    session.commit()
    run_ids.append(run.id)

    # List discovery runs
    res_runs = client.get("/api/v1/discovery/runs")
    assert res_runs.status_code == 200
    assert len(res_runs.json()) >= 1

    # Add candidate endpoint
    cand = SourceEndpoint(source_id=source.id, url="https://gov.in/new-report.pdf", method="GET", status="CANDIDATE")
    session.add(cand)
    session.commit()
    endpoint_ids.append(cand.id)

    # Approve candidate
    res_app = client.post(f"/api/v1/discovery/candidates/{cand.id}/approve")
    assert res_app.status_code == 200

def test_ingestion_batches_api(db):
    session, source_ids, endpoint_ids, run_ids, dataset_ids, batch_ids = db
    
    source = Source(name="Ingestion Batch Test Source", status="ACTIVE")
    session.add(source)
    session.commit()
    source_ids.append(source.id)

    # Create ingestion batch
    res_create = client.post("/api/v1/ingestion/batches", json=[str(source.id)])
    assert res_create.status_code == 200
    batch_id = res_create.json()["batch_id"]
    batch_ids.append(uuid.UUID(batch_id))

    # Get batch detail
    res_detail = client.get(f"/api/v1/ingestion/batches/{batch_id}")
    assert res_detail.status_code == 200
    assert res_detail.json()["status"] == "CREATED"

    # List batches
    res_list = client.get("/api/v1/ingestion/batches")
    assert res_list.status_code == 200
    assert len(res_list.json()) >= 1

def test_coverage_summary_api(db):
    res_cov = client.get("/api/v1/coverage")
    assert res_cov.status_code == 200
    assert "national_coverage_percentage" in res_cov.json()
