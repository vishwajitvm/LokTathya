from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from models.source import IngestionRun, SourceEndpoint, Dataset
from datetime import datetime
from tracenest import logger
import uuid

router = APIRouter(prefix="/api/v1/discovery", tags=["Discovery Engine"])

@router.post("/run")
def trigger_discovery_run(source_id: uuid.UUID, max_pages: int = 50, db: Session = Depends(get_db)):
    logger.info("POST /api/v1/discovery/run – Triggering link discovery", source_id=str(source_id))
    
    # Check or create default dataset
    dataset = db.query(Dataset).filter(Dataset.source_id == source_id).first()
    if not dataset:
        dataset = Dataset(source_id=source_id, name="Default Dataset")
        db.add(dataset)
        db.flush()
        
    run = IngestionRun(
        dataset_id=dataset.id,
        started_at=datetime.utcnow(),
        status="RUNNING"
    )
    db.add(run)
    db.commit()
    
    return {
        "run_id": str(run.id),
        "source_id": str(source_id),
        "status": run.status,
        "max_pages": max_pages
    }

@router.get("/runs/{run_id}")
def get_discovery_run_status(run_id: uuid.UUID, db: Session = Depends(get_db)):
    logger.info("GET /api/v1/discovery/runs/{id} – Checking run status", run_id=str(run_id))
    run = db.query(IngestionRun).filter(IngestionRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Ingestion run not found")
        
    return {
        "run_id": str(run.id),
        "status": run.status,
        "started_at": run.started_at
    }

@router.get("/candidates")
def get_discovery_candidates(db: Session = Depends(get_db)):
    logger.info("GET /api/v1/discovery/candidates – Fetching candidate URLs")
    # Retrieve endpoints with status = CANDIDATE
    candidates = db.query(SourceEndpoint).filter(SourceEndpoint.status == "CANDIDATE").all()
    return [
        {
            "id": str(c.id),
            "url": c.url,
            "type": c.expected_format or "UNKNOWN",
            "discovered_at": c.observed_at
        }
        for c in candidates
    ]

@router.get("/runs")
def list_discovery_runs(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    runs = db.query(IngestionRun).offset(offset).limit(limit).all()
    return [
        {
            "id": str(r.id),
            "dataset_id": str(r.dataset_id),
            "started_at": r.started_at,
            "status": r.status
        }
        for r in runs
    ]

@router.post("/runs")
def trigger_discovery_runs_path(source_id: uuid.UUID, max_pages: int = 50, db: Session = Depends(get_db)):
    return trigger_discovery_run(source_id, max_pages, db)

@router.post("/candidates/{id}/approve")
def approve_candidate(id: uuid.UUID, db: Session = Depends(get_db)):
    ep = db.query(SourceEndpoint).filter(SourceEndpoint.id == id).first()
    if not ep:
        raise HTTPException(status_code=404, detail="Candidate not found")
    ep.status = "ACTIVE"
    db.commit()
    return {"status": "SUCCESS", "candidate_id": str(id)}

@router.post("/candidates/{id}/reject")
def reject_candidate(id: uuid.UUID, db: Session = Depends(get_db)):
    ep = db.query(SourceEndpoint).filter(SourceEndpoint.id == id).first()
    if not ep:
        raise HTTPException(status_code=404, detail="Candidate not found")
    ep.status = "DISABLED"
    db.commit()
    return {"status": "SUCCESS", "candidate_id": str(id)}
