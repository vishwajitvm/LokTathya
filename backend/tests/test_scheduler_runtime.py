import pytest
from datetime import datetime, timezone, timedelta
from ingestion.tasks import poll_scheduler
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

def test_poll_scheduler_runtime(db_session: Session):
    source = Source(name="Runtime Scheduler Test Source", status="ACTIVE")
    db_session.add(source)
    db_session.commit()

    # Create endpoint that is due
    endpoint = SourceEndpoint(
        source_id=source.id,
        url="https://scheduler.gov.in/runtime-test.json",
        method="GET",
        refresh_frequency="HOURLY",
        next_scheduled_at=datetime.now(timezone.utc) - timedelta(minutes=5),
        enabled=True,
        status="ACTIVE"
    )
    db_session.add(endpoint)
    db_session.commit()

    # Trigger poll_scheduler task
    res = poll_scheduler.apply()
    assert res.result["status"] == "SUCCESS"
    assert res.result["triggered_count"] >= 1

    # Reload from DB and check next schedule is set to future
    db_session.refresh(endpoint)
    assert endpoint.next_scheduled_at > datetime.now(timezone.utc)
    assert endpoint.last_checked is not None
