from sqlalchemy.orm import Session
from models.source import Source, SourceEndpoint
from schemas.source_schema import SourceCreate, EndpointCreate
import uuid

class SourceService:
    @staticmethod
    def create_source(db: Session, source: SourceCreate):
        db_source = Source(**source.model_dump())
        db.add(db_source)
        db.commit()
        db.refresh(db_source)
        return db_source

    @staticmethod
    def get_source(db: Session, source_id: uuid.UUID):
        return db.query(Source).filter(Source.id == source_id).first()

    @staticmethod
    def list_sources(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Source).offset(skip).limit(limit).all()

    @staticmethod
    def update_source_status(db: Session, source_id: uuid.UUID, status: str):
        db_source = db.query(Source).filter(Source.id == source_id).first()
        if db_source:
            db_source.status = status
            db.commit()
            db.refresh(db_source)
        return db_source
