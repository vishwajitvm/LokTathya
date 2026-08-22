from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from tracenest import logger
import uuid

router = APIRouter(prefix="/api/v1/quarantine", tags=["Quarantine Management"])

@router.get("")
def list_quarantine_items(db: Session = Depends(get_db)):
    logger.info("GET /api/v1/quarantine – Listing items in quarantine")
    return [
        {
            "id": str(uuid.uuid4()),
            "source_id": str(uuid.uuid4()),
            "artifact_path": "raw/malformed.pdf",
            "error_type": "PDFParserError",
            "message": "EOF marker not found",
            "status": "QUARANTINED",
            "observed_at": "2026-08-22T18:00:00Z"
        }
    ]

@router.get("/{quarantine_id}")
def get_quarantine_item(quarantine_id: uuid.UUID, db: Session = Depends(get_db)):
    logger.info("GET /api/v1/quarantine/{id} – Fetching quarantine detail", quarantine_id=str(quarantine_id))
    return {
        "id": str(quarantine_id),
        "source_id": str(uuid.uuid4()),
        "artifact_path": "raw/malformed.pdf",
        "error_type": "PDFParserError",
        "message": "EOF marker not found",
        "status": "QUARANTINED",
        "observed_at": "2026-08-22T18:00:00Z",
        "stack_trace": "Traceback (most recent call): ... PDFReader fail"
    }

@router.post("/{quarantine_id}/retry")
def retry_quarantine_item(quarantine_id: uuid.UUID, db: Session = Depends(get_db)):
    logger.info("POST /api/v1/quarantine/{id}/retry – Triggering retry", quarantine_id=str(quarantine_id))
    return {
        "id": str(quarantine_id),
        "status": "RETRY_PENDING"
    }

@router.post("/{quarantine_id}/resolve")
def resolve_quarantine_item(quarantine_id: uuid.UUID, db: Session = Depends(get_db)):
    logger.info("POST /api/v1/quarantine/{id}/resolve – Mark resolved", quarantine_id=str(quarantine_id))
    return {
        "id": str(quarantine_id),
        "status": "RESOLVED"
    }
