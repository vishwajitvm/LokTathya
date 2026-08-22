import pytest
import uuid
from services.canonicalizer import CanonicalizationFactory
from models.source import Source, Document, ContentVersion
from models.observation import Observation
from models.provenance import CanonicalFact, Claim, Evidence
from sqlalchemy.orm import Session
from core.database import SessionLocal

@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    try:
        db.query(Evidence).delete()
        db.query(Claim).delete()
        db.query(CanonicalFact).delete()
        db.query(Observation).delete()
        db.commit()
        yield db
    finally:
        db.close()

def test_canonicalize_observation_pipeline(db_session: Session):
    source = Source(name="Canonicalizer Test Source", status="ACTIVE")
    db_session.add(source)
    db_session.commit()

    doc = Document(source_id=source.id, title="Test Report")
    db_session.add(doc)
    db_session.commit()

    cv = ContentVersion(
        document_id=doc.id,
        version_number=1,
        sha256="canonicalizer_test_hash",
        storage_path="raw/path/doc.pdf"
    )
    db_session.add(cv)
    db_session.commit()

    # Create raw observation
    obs = Observation(
        source_id=source.id,
        document_id=doc.id,
        content_version_id=cv.id,
        entity_type="budget_allocation",
        field_name="defense_expenditure",
        raw_value="₹1,25,000",
        status="VALIDATED"
    )
    db_session.add(obs)
    db_session.commit()

    factory = CanonicalizationFactory(db_session)
    fact_id = factory.process_observation(obs.id)
    assert fact_id is not None

    # Load canonical fact from DB and check value normalisation
    fact = db_session.query(CanonicalFact).filter(CanonicalFact.id == fact_id).first()
    assert fact is not None
    assert fact.attribute_name == "defense_expenditure"
    assert fact.value["value"] == 125000.0

    # Verify Provenance mappings
    claim = db_session.query(Claim).filter(Claim.canonical_fact_id == fact_id).first()
    assert claim is not None
    
    evidence = db_session.query(Evidence).filter(Evidence.claim_id == claim.id).first()
    assert evidence is not None
    assert evidence.source_id == source.id
    assert evidence.document_id == doc.id
