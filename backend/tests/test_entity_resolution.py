import pytest
import uuid
from entity_resolution.engine import EntityResolutionEngine
from models.resolution import EntityResolution
from models.source import Source
from sqlalchemy.orm import Session
from core.database import SessionLocal

@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_resolve_exact_match(db_session: Session):
    source = Source(name="Resolution Test Source", status="ACTIVE")
    db_session.add(source)
    db_session.commit()

    candidate_uuid = uuid.uuid4()
    target_tbl = f"reps_{uuid.uuid4()}"
    # Insert seed resolution
    res_entry = EntityResolution(
        source_id=source.id,
        raw_value="Shri Narendra Modi",
        target_table=target_tbl,
        candidate_id=candidate_uuid,
        matching_method="seed",
        confidence=1.0,
        status="CONFIRMED"
    )
    db_session.add(res_entry)
    db_session.commit()

    engine = EntityResolutionEngine(db_session)
    
    # Test exact resolution
    res = engine.resolve_entity("Shri Narendra Modi", target_tbl, source.id)
    assert res["status"] == "RESOLVED"
    assert res["method"] == "exact_match"
    assert res["matched_entity_id"] == candidate_uuid

    # Test normalized exact match (lowercase variant)
    res_norm = engine.resolve_entity("shri narendra modi", target_tbl, source.id)
    assert res_norm["status"] == "RESOLVED"
    assert res_norm["method"] == "normalized_exact_match"

    # Test fuzzy match
    res_fuzzy = engine.resolve_entity("Narendra Modi", target_tbl, source.id)
    assert res_fuzzy["status"] == "PROBABLE"
    assert res_fuzzy["method"] == "fuzzy_match"
