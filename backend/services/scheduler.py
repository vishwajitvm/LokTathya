import random
import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from models.source import Source, SourceEndpoint

class SourceScheduler:
    """
    Step 3: Source Scheduling Engine.
    Handles next scheduled calculation, exponential backoff, jitter, and execution triggers.
    """
    
    @staticmethod
    def calculate_next_run(frequency: str, last_run: datetime) -> datetime:
        if frequency == "HOURLY":
            return last_run + timedelta(hours=1)
        elif frequency == "DAILY":
            return last_run + timedelta(days=1)
        elif frequency == "WEEKLY":
            return last_run + timedelta(weeks=1)
        elif frequency == "MONTHLY":
            return last_run + timedelta(days=30)
        else:
            # Default fallback to 24 hours
            return last_run + timedelta(days=1)

    @staticmethod
    def calculate_backoff_delay(retry_count: int, base_delay_seconds: int = 300) -> int:
        """Calculate exponential backoff delay with jitter."""
        factor = 2 ** retry_count
        delay = base_delay_seconds * factor
        # Add random jitter up to +/- 20%
        jitter = random.uniform(0.8, 1.2)
        return int(delay * jitter)

    @classmethod
    def schedule_due_endpoints(cls, db: Session) -> int:
        """
        Check for endpoints that are enabled and past their scheduled time.
        Queue Celery task for execution and update schedules.
        """
        now = datetime.now(timezone.utc)
        due_endpoints = db.query(SourceEndpoint).filter(
            SourceEndpoint.enabled == True,
            SourceEndpoint.status != "DISABLED",
            (SourceEndpoint.next_scheduled_at == None) | (SourceEndpoint.next_scheduled_at <= now)
        ).all()

        triggered_count = 0
        for endpoint in due_endpoints:
            # Update next schedule
            last_ref = endpoint.last_checked or now
            freq = endpoint.refresh_frequency or "DAILY"
            endpoint.next_scheduled_at = cls.calculate_next_run(freq, last_ref)
            endpoint.last_checked = now
            triggered_count += 1

        if triggered_count > 0:
            db.commit()
            
        return triggered_count

    @classmethod
    def handle_fetch_failure(cls, db: Session, endpoint_id: uuid.UUID, error_message: str):
        """Update failure state, compute next backoff retry scheduled time."""
        endpoint = db.query(SourceEndpoint).filter(SourceEndpoint.id == endpoint_id).first()
        if not endpoint:
            return

        endpoint.error_count = (endpoint.error_count or 0) + 1
        endpoint.retry_count = (endpoint.retry_count or 0) + 1
        endpoint.last_failure = datetime.now(timezone.utc)

        if endpoint.retry_count >= 5:
            # Degrade status after repeated failures
            endpoint.status = "DEGRADED"
            endpoint.enabled = False
        else:
            delay_seconds = cls.calculate_backoff_delay(endpoint.retry_count)
            endpoint.next_scheduled_at = datetime.now(timezone.utc) + timedelta(seconds=delay_seconds)

        db.commit()

    @classmethod
    def handle_fetch_success(cls, db: Session, endpoint_id: uuid.UUID):
        """Reset retry counts and failures upon successful fetch."""
        endpoint = db.query(SourceEndpoint).filter(SourceEndpoint.id == endpoint_id).first()
        if not endpoint:
            return

        endpoint.error_count = 0
        endpoint.retry_count = 0
        endpoint.last_success = datetime.now(timezone.utc)
        endpoint.status = "ACTIVE"
        
        freq = endpoint.refresh_frequency or "DAILY"
        endpoint.next_scheduled_at = cls.calculate_next_run(freq, datetime.now(timezone.utc))
        db.commit()
