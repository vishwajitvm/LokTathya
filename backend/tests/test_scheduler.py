import pytest
from datetime import datetime, timezone, timedelta
from services.scheduler import SourceScheduler
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

def test_calculate_next_run():
    last_run = datetime(2026, 8, 22, 12, 0, 0, tzinfo=timezone.utc)
    
    hourly = SourceScheduler.calculate_next_run("HOURLY", last_run)
    assert hourly == last_run + timedelta(hours=1)
    
    daily = SourceScheduler.calculate_next_run("DAILY", last_run)
    assert daily == last_run + timedelta(days=1)
    
    weekly = SourceScheduler.calculate_next_run("WEEKLY", last_run)
    assert weekly == last_run + timedelta(weeks=1)

def test_calculate_backoff_delay():
    delay_1 = SourceScheduler.calculate_backoff_delay(1, base_delay_seconds=10)
    # 10 * 2 = 20, jitter +/- 20% -> [16, 24]
    assert 16 <= delay_1 <= 24

def test_schedule_due_endpoints(db_session: Session):
    source = Source(name="Scheduler Test Source", status="ACTIVE")
    db_session.add(source)
    db_session.commit()

    # Create endpoint that is due
    endpoint = SourceEndpoint(
        source_id=source.id,
        url="https://scheduler.gov.in/data.json",
        method="GET",
        refresh_frequency="DAILY",
        next_scheduled_at=datetime.now(timezone.utc) - timedelta(minutes=10),
        enabled=True,
        status="ACTIVE"
    )
    db_session.add(endpoint)
    db_session.commit()

    triggered = SourceScheduler.schedule_due_endpoints(db_session)
    assert triggered >= 1

    # Reload from DB and check next schedule is set to future
    db_session.refresh(endpoint)
    assert endpoint.next_scheduled_at > datetime.now(timezone.utc)
    assert endpoint.last_checked is not None
