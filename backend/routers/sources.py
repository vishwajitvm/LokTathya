from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.source_schema import SourceCreate, SourceResponse
from services.source_service import SourceService
from core.database import get_db

router = APIRouter(prefix="/api/v1/sources", tags=["Sources"])

@router.post("/", response_model=SourceResponse)
def create_source(source: SourceCreate, db: Session = Depends(get_db)):
    return SourceService.create_source(db, source)

@router.get("/", response_model=list[SourceResponse])
def list_sources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return SourceService.list_sources(db, skip=skip, limit=limit)
