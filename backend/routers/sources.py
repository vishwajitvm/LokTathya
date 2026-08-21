from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.source_schema import SourceCreate, SourceResponse
from services.source_service import SourceService
# Assuming a get_db dependency exists in core
# from core.database import get_db

router = APIRouter(prefix="/api/v1/sources", tags=["Sources"])

# Mock get_db for now
def get_db():
    yield None

@router.post("/", response_model=SourceResponse)
def create_source(source: SourceCreate, db: Session = Depends(get_db)):
    # db is mocked
    return SourceService.create_source(db, source)

@router.get("/", response_model=list[SourceResponse])
def list_sources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return SourceService.list_sources(db, skip=skip, limit=limit)
