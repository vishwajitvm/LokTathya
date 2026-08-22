from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from tracenest import logger
from ingestion.batch import IngestionBatchManager
from models.source import IngestionBatch
from core.database import get_db
import uuid

router = APIRouter(prefix="/api/v1/ingestion", tags=["Ingestion Dashboard"])

@router.post("/batches")
def trigger_batch(source_ids: list[str], scope: str = "national", db: Session = Depends(get_db)):
    logger.info("POST /api/v1/ingestion/batches – Triggering new ingestion batch", source_count=len(source_ids), scope=scope)
    try:
        manager = IngestionBatchManager(db)
        result = manager.create_batch(source_ids, scope)
        logger.info("Ingestion batch triggered successfully", batch_id=result["batch_id"])
        return result
    except Exception as e:
        logger.error("Ingestion batch trigger FAILED", source_ids=str(source_ids), scope=scope, error=str(e))
        raise

@router.get("/batches")
def list_batches(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    batches = db.query(IngestionBatch).offset(offset).limit(limit).all()
    return [
        {
            "id": str(b.id),
            "scope": b.scope,
            "source_ids": b.source_ids.get("source_ids", []),
            "status": b.status,
            "created_at": b.created_at
        }
        for b in batches
    ]

@router.get("/batches/{batch_id}")
def get_batch(batch_id: uuid.UUID, db: Session = Depends(get_db)):
    b = db.query(IngestionBatch).filter(IngestionBatch.id == batch_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Batch not found")
    return {
        "id": str(b.id),
        "scope": b.scope,
        "source_ids": b.source_ids.get("source_ids", []),
        "status": b.status,
        "created_at": b.created_at
    }

@router.get("/metrics")
def get_ingestion_metrics():
    logger.info("GET /api/v1/ingestion/metrics – Fetching ingestion pipeline metrics")
    metrics = {
        "sources_scheduled": 5,
        "successful_fetches": 4,
        "failed_fetches": 1,
        "unchanged_content": 2,
        "new_content_versions": 2,
        "documents_parsed": 2,
        "parse_failures": 1,
        "canonical_records": 15000,
        "quarantined_records": 42
    }
    return metrics
