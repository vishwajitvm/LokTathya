from sqlalchemy.orm import Session
from tracenest import logger
from models.source import Source, SourceEndpoint
from schemas.source_schema import SourceCreate, EndpointCreate
import uuid

class SourceService:
    @staticmethod
    def create_source(db: Session, source: SourceCreate):
        logger.info("SourceService.create_source – Persisting new source to database", source_name=source.name)
        logger.debug("Dumping source model to dict for ORM insert", source_type=source.source_type)
        db_source = Source(**source.model_dump())
        logger.debug("ORM Source object created, adding to session", source_id=str(db_source.id))
        db.add(db_source)
        logger.debug("Committing transaction to database")
        db.commit()
        db.refresh(db_source)
        logger.info("Source persisted successfully", source_id=str(db_source.id), source_name=db_source.name)
        return db_source

    @staticmethod
    def get_source(db: Session, source_id: uuid.UUID):
        logger.info("SourceService.get_source – Fetching source by ID", source_id=str(source_id))
        result = db.query(Source).filter(Source.id == source_id).first()
        if result:
            logger.info("Source found", source_id=str(source_id), source_name=result.name)
        else:
            logger.warning("Source NOT FOUND", source_id=str(source_id))
        return result

    @staticmethod
    def list_sources(db: Session, skip: int = 0, limit: int = 100):
        logger.info("SourceService.list_sources – Querying all sources", skip=skip, limit=limit)
        logger.debug("Executing SELECT on Source table", offset=skip, limit=limit)
        results = db.query(Source).offset(skip).limit(limit).all()
        logger.info("Sources query completed", count=len(results))
        return results

    @staticmethod
    def update_source_status(db: Session, source_id: uuid.UUID, status: str):
        logger.info("SourceService.update_source_status – Updating source status", source_id=str(source_id), new_status=status)
        db_source = db.query(Source).filter(Source.id == source_id).first()
        if db_source:
            old_status = getattr(db_source, 'status', 'unknown')
            db_source.status = status
            db.commit()
            db.refresh(db_source)
            logger.info("Source status updated", source_id=str(source_id), old_status=str(old_status), new_status=status)
        else:
            logger.warning("Source NOT FOUND for status update", source_id=str(source_id))
        return db_source
