import pytest
import uuid
from fastapi.testclient import TestClient
from main import app
from core.database import SessionLocal
from models.geography import Geography
from models.representative import Person, Term, Position, Party
from models.election import Election, ElectionEvent, ElectionResult, Candidate
from models.project import Project
from models.finance import Budget

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def test_location_and_profile_api(db):
    # Test NOT_COMPUTABLE for unresolved coordinate
    response = client.get("/api/v1/location/resolve?latitude=10.0&longitude=20.0")
    assert response.status_code in (400, 404)
    assert response.json()["detail"] == "NOT_COMPUTABLE"

    # Test geography detail and children
    geo_id = uuid.uuid4()
    geo = Geography(id=geo_id, type="State", name="Test State Geoposition")
    db.add(geo)
    db.commit()

    res_prof = client.get(f"/api/v1/location/{geo_id}/profile")
    assert res_prof.status_code == 200
    assert res_prof.json()["geography"]["name"] == "Test State Geoposition"

def test_geographies_list_api(db):
    response = client.get("/api/v1/geographies")
    assert response.status_code == 200
    assert "data" in response.json()

def test_representatives_list_api(db):
    response = client.get("/api/v1/representatives")
    assert response.status_code == 200

def test_elections_list_api(db):
    response = client.get("/api/v1/elections")
    assert response.status_code == 200

def test_projects_list_api(db):
    response = client.get("/api/v1/projects")
    assert response.status_code == 200

def test_finance_budgets_list_api(db):
    response = client.get("/api/v1/finance/budgets")
    assert response.status_code == 200

def test_search_api(db):
    response = client.get("/api/v1/search?query=test")
    assert response.status_code == 200
