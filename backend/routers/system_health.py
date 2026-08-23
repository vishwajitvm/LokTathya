from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from core.database import get_db
from models.source import Source, SourceEndpoint, IngestionRun, Quarantine
from datetime import datetime, timedelta, timezone

router = APIRouter(prefix="/api/v1/health", tags=["System Health"])

@router.get("/metrics")
def get_system_metrics(db: Session = Depends(get_db)):
    """System-wide health and ingestion metrics."""
    # Source metrics
    active_sources = db.query(Source).filter(Source.status == "ACTIVE").count()
    degraded_sources = db.query(Source).filter(Source.health_status == "DEGRADED").count()
    
    # Endpoint metrics
    active_endpoints = db.query(SourceEndpoint).filter(SourceEndpoint.status == "ACTIVE").count()
    candidates = db.query(SourceEndpoint).filter(SourceEndpoint.status == "CANDIDATE").count()
    
    # Ingestion metrics
    now = datetime.now(timezone.utc)
    recent_runs = db.query(IngestionRun).filter(IngestionRun.started_at >= now - timedelta(hours=24)).count()
    failed_runs = db.query(IngestionRun).filter(
        IngestionRun.started_at >= now - timedelta(hours=24),
        IngestionRun.status == "FAILED"
    ).count()
    
    quarantine_count = db.query(Quarantine).filter(Quarantine.status == "QUARANTINED").count()

    return {
        "status": "HEALTHY",
        "timestamp": now.isoformat(),
        "sources": {
            "active": active_sources,
            "degraded": degraded_sources
        },
        "endpoints": {
            "active": active_endpoints,
            "candidates": candidates
        },
        "ingestion": {
            "runs_24h": recent_runs,
            "failed_runs_24h": failed_runs,
            "quarantined_items": quarantine_count
        }
    }
