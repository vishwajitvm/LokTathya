from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.source import SourceHistory
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/v1/sources/{source_id}/history", tags=["Source History"])

@router.get("/")
def list_source_history(source_id: uuid.UUID, limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    """List historical snapshots of a source."""
    records = db.query(SourceHistory).filter(
        SourceHistory.source_id == source_id
    ).order_by(SourceHistory.created_at.desc()).offset(offset).limit(limit).all()
    
    return [
        {
            "id": str(r.id),
            "source_id": str(r.source_id),
            "snapshot": r.snapshot,
            "change_reason": r.change_reason,
            "created_at": r.created_at
        }
        for r in records
    ]
