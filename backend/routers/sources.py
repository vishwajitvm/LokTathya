from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from tracenest import logger
from schemas.source_schema import SourceCreate, SourceResponse
from services.source_service import SourceService
from core.database import get_db
from models.source import Source, SourceEndpoint, Document, ContentVersion
import uuid
from typing import Optional

router = APIRouter(prefix="/api/v1/sources", tags=["Sources"])

@router.post("/", response_model=SourceResponse)
def create_source(source: SourceCreate, db: Session = Depends(get_db)):
    logger.info("POST /api/v1/sources – Creating new data source", source_name=source.name, source_type=source.source_type)
    logger.debug("Database session acquired for source creation", session_id=str(id(db)))
    try:
        result = SourceService.create_source(db, source)
        logger.info("Source created successfully", source_id=str(result.id), source_name=result.name)
        return result
    except Exception as e:
        logger.error("Source creation FAILED", source_name=source.name, error=str(e))
        raise

@router.get("/", response_model=list[SourceResponse])
def list_sources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info("GET /api/v1/sources – Listing data sources", skip=skip, limit=limit)
    logger.debug("Database session acquired for source listing", session_id=str(id(db)))
    try:
        results = SourceService.list_sources(db, skip=skip, limit=limit)
        logger.info("Sources listed successfully", source_count=len(results))
        return results
    except Exception as e:
        logger.error("Source listing FAILED", error=str(e))
        raise

@router.get("/{source_id}/history")
def get_source_history(source_id: uuid.UUID, db: Session = Depends(get_db)):
    # Mocking response
    source = db.query(Source).get(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    return {
        "source_id": str(source.id),
        "history": [
            {
                "status": source.status,
                "updated_at": source.updated_at,
                "authority_name": source.authority_name
            }
        ]
    }

@router.get("/documents/{document_id}/versions")
def get_document_versions(document_id: uuid.UUID, observed_at: Optional[str] = Query(None), db: Session = Depends(get_db)):
    doc = db.query(Document).get(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    versions = db.query(ContentVersion).filter(ContentVersion.document_id == document_id).order_by(ContentVersion.version_number.desc()).all()
    
    return {
        "document_id": str(doc.id),
        "status": doc.status,
        "versions": [
            {
                "version_number": v.version_number,
                "sha256": v.sha256,
                "created_at": v.created_at
            }
            for v in versions
        ]
    }

@router.get("/documents/{document_id}/diff")
def get_document_diff(document_id: uuid.UUID, v1: int, v2: int, db: Session = Depends(get_db)):
    return {
        "status": "MODIFIED",
        "diff": {
            "text_diff": {"similarity_ratio": 0.8},
            "table_diff": {"added": [], "removed": []},
            "pages_added": 0,
            "pages_removed": 0
        }
    }
