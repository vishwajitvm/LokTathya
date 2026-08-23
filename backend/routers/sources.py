from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from tracenest import logger
from schemas.source_schema import SourceCreate, SourceResponse
from services.source_service import SourceService
from core.database import get_db
from models.source import Source, SourceEndpoint, Document, ContentVersion
import uuid
from datetime import datetime
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

@router.get("/{source_id}", response_model=SourceResponse)
def get_source(source_id: uuid.UUID, db: Session = Depends(get_db)):
    logger.info("GET /api/v1/sources/{source_id} – Fetching data source", source_id=str(source_id))
    result = SourceService.get_source(db, source_id)
    if not result:
        raise HTTPException(status_code=404, detail="Source not found")
    return result

@router.get("/{source_id}/endpoints")
def get_source_endpoints(source_id: uuid.UUID, db: Session = Depends(get_db)):
    logger.info("GET /api/v1/sources/{source_id}/endpoints – Listing source endpoints", source_id=str(source_id))
    source = SourceService.get_source(db, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    endpoints = db.query(SourceEndpoint).filter(SourceEndpoint.source_id == source_id).all()
    return [
        {
            "id": str(ep.id),
            "url": ep.url,
            "method": ep.method,
            "status": ep.status,
            "redirect_url": ep.redirect_url,
            "observed_at": ep.observed_at
        }
        for ep in endpoints
    ]



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
    doc = db.query(Document).get(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    cv1 = db.query(ContentVersion).filter(ContentVersion.document_id == document_id, ContentVersion.version_number == v1).first()
    cv2 = db.query(ContentVersion).filter(ContentVersion.document_id == document_id, ContentVersion.version_number == v2).first()
    
    if not cv1 or not cv2:
        raise HTTPException(status_code=404, detail="One or both content versions not found")

    # Load content from MinIO and run real diff check
    from storage.minio_client import MinIOStorageService
    from ingestion.diff_engine import DocumentDiffEngine
    
    storage = MinIOStorageService()
    text_a = ""
    text_b = ""
    
    try:
        if cv1.storage_path and storage.exists(cv1.storage_path):
            data_a = storage.get(cv1.storage_path)
            text_a = data_a.decode('utf-8', errors='ignore') if data_a else ""
        if cv2.storage_path and storage.exists(cv2.storage_path):
            data_b = storage.get(cv2.storage_path)
            text_b = data_b.decode('utf-8', errors='ignore') if data_b else ""
    except Exception as e:
        logger.error("Failed to load version content for diffing", error=str(e))

    engine = DocumentDiffEngine()
    diff_res = engine.diff_documents({"text": text_a}, {"text": text_b})
    return diff_res

@router.patch("/{id}")
def update_source(id: uuid.UUID, updates: dict, db: Session = Depends(get_db)):
    source = db.query(Source).filter(Source.id == id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    for k, v in updates.items():
        if hasattr(source, k):
            setattr(source, k, v)
    db.commit()
    return {"status": "SUCCESS", "source_id": str(id)}

from pydantic import BaseModel

class EndpointCreate(BaseModel):
    url: str
    method: str = "GET"
    rate_limit_rpm: Optional[int] = None

@router.post("/{id}/endpoints")
def create_source_endpoint(id: uuid.UUID, endpoint: EndpointCreate, db: Session = Depends(get_db)):
    source = db.query(Source).filter(Source.id == id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
        
    ep = SourceEndpoint(
        source_id=id,
        url=endpoint.url,
        method=endpoint.method,
        rate_limit_rpm=endpoint.rate_limit_rpm,
        status="ACTIVE",
        observed_at=datetime.utcnow()
    )
    db.add(ep)
    db.commit()
    return {"status": "SUCCESS", "endpoint_id": str(ep.id), "rate_limit_rpm": ep.rate_limit_rpm}

@router.patch("/endpoints/{ep_id}")
def update_source_endpoint(ep_id: uuid.UUID, updates: dict, db: Session = Depends(get_db)):
    ep = db.query(SourceEndpoint).filter(SourceEndpoint.id == ep_id).first()
    if not ep:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    for k, v in updates.items():
        if hasattr(ep, k):
            setattr(ep, k, v)
    db.commit()
    return {"status": "SUCCESS", "endpoint_id": str(ep_id)}
