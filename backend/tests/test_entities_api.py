import pytest
import uuid
from fastapi.testclient import TestClient
from main import app
from core.database import SessionLocal
from models.source import Source, Document, ContentVersion
from models.observation import Observation
from models.provenance import CanonicalFact, Claim, Evidence
from models.resolution import EntityResolution

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    session = SessionLocal()
    try:
        session.query(Evidence).delete()
        session.query(Claim).delete()
        session.query(CanonicalFact).delete()
        session.query(Observation).delete()
        session.query(EntityResolution).delete()
        session.commit()
        yield session
    finally:
        session.close()

def test_list_entities_api(db):
    source = Source(name="API Entity Test Source", status="ACTIVE")
    db.add(source)
    db.commit()

    candidate_id = uuid.uuid4()
    res = EntityResolution(
        source_id=source.id,
        raw_value="Representative Modi",
        target_table="reps",
        candidate_id=candidate_id,
        matching_method="fuzzy",
        confidence=0.9,
        status="HUMAN_REVIEW"
    )
    db.add(res)
    db.commit()

    response = client.get("/api/v1/entities")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["raw_value"] == "Representative Modi"

    # Detail API
    res_det = client.get(f"/api/v1/entities/{candidate_id}")
    assert res_det.status_code == 200
    assert res_det.json()["raw_value"] == "Representative Modi"

def test_pending_reviews_api(db):
    response = client.get("/api/v1/entity-resolution/reviews")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["status"] == "HUMAN_REVIEW"

    # Resolve review item
    review_id = data[0]["id"]
    new_uuid = uuid.uuid4()
    res_post = client.post(f"/api/v1/entity-resolution/reviews/{review_id}/resolve?matched_entity_id={new_uuid}")
    assert res_post.status_code == 200
    assert res_post.json()["status"] == "SUCCESS"
