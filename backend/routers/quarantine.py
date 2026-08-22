from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.source import Quarantine
from tracenest import logger
import uuid

router = APIRouter(prefix="/api/v1/quarantine", tags=["Quarantine Management"])

@router.get("")
def list_quarantine_items(db: Session = Depends(get_db)):
    logger.info("GET /api/v1/quarantine – Listing items in quarantine")
    items = db.query(Quarantine).all()
    return [
        {
            "id": str(item.id),
            "source_id": str(item.source_id) if item.source_id else None,
            "artifact_path": item.artifact_path,
            "error_type": item.error_type,
            "message": item.message,
            "status": item.status,
            "observed_at": item.created_at
        }
        for item in items
    ]

@router.get("/{quarantine_id}")
def get_quarantine_item(quarantine_id: uuid.UUID, db: Session = Depends(get_db)):
    logger.info("GET /api/v1/quarantine/{id} – Fetching quarantine detail", quarantine_id=str(quarantine_id))
    item = db.query(Quarantine).filter(Quarantine.id == quarantine_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Quarantine record not found")
        
    return {
        "id": str(item.id),
        "source_id": str(item.source_id) if item.source_id else None,
        "artifact_path": item.artifact_path,
        "error_type": item.error_type,
        "message": item.message,
        "status": item.status,
        "observed_at": item.created_at,
        "stack_trace": item.stack_trace
    }

@router.post("/{quarantine_id}/retry")
def retry_quarantine_item(quarantine_id: uuid.UUID, db: Session = Depends(get_db)):
    logger.info("POST /api/v1/quarantine/{id}/retry – Triggering retry", quarantine_id=str(quarantine_id))
    item = db.query(Quarantine).filter(Quarantine.id == quarantine_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Quarantine record not found")
        
    item.status = "RETRY_PENDING"
    db.commit()
    return {
        "id": str(item.id),
        "status": item.status
    }

@router.post("/{quarantine_id}/resolve")
def resolve_quarantine_item(quarantine_id: uuid.UUID, db: Session = Depends(get_db)):
    logger.info("POST /api/v1/quarantine/{id}/resolve – Mark resolved", quarantine_id=str(quarantine_id))
    item = db.query(Quarantine).filter(Quarantine.id == quarantine_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Quarantine record not found")
        
    item.status = "RESOLVED"
    db.commit()
    return {
        "id": str(item.id),
        "status": item.status
    }
