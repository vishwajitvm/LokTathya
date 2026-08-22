from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from tracenest import logger
from schemas.source_schema import SourceCreate, SourceResponse
from services.source_service import SourceService
from core.database import get_db

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
