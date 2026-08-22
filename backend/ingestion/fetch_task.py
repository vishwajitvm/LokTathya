import hashlib
import time
from datetime import datetime
from uuid import UUID
from core.http_client import ResilientHTTPClient
from models.source import FetchEvent, ContentVersion, SourceEndpoint, Document
from sqlalchemy.orm import Session
from tracenest import logger

class StorageService:
    """Mock storage service for Priority 1 simulation."""
    def put(self, path: str, content: bytes):
        pass

def process_endpoint_fetch(db: Session, endpoint_id: UUID, run_id: UUID):
    """
    Priority 1 Celery Task execution logic for fetching.
    """
    logger.info("Starting fetch for endpoint", endpoint_id=str(endpoint_id))
    
    endpoint = db.query(SourceEndpoint).get(endpoint_id)
    if not endpoint:
        logger.error("Endpoint not found", endpoint_id=str(endpoint_id))
        return None

    # Retrieve last fetch event for ETag and Last-Modified
    last_event = db.query(FetchEvent).filter(
        FetchEvent.endpoint_id == endpoint_id,
        FetchEvent.status_code == 200
    ).order_by(FetchEvent.fetched_at.desc()).first()

    etag = last_event.etag if last_event else None
    last_mod = last_event.last_modified if last_event else None

    # Create new event
    new_event = FetchEvent(
        endpoint_id=endpoint.id,
        run_id=run_id,
        url=endpoint.url,
        fetched_at=datetime.utcnow()
    )
    db.add(new_event)
    
    client = ResilientHTTPClient(timeout=10)
    
    # Synchronous wrapper for demonstration of business logic inside task
    # Real implementation uses asyncio.run or async Celery workers
    import asyncio
    result = asyncio.run(client.fetch(endpoint.url, etag=etag, last_modified=last_mod))
    
    if result["status"] == "NOT_MODIFIED":
        new_event.status_code = 304
        logger.info("Content unchanged (304)", endpoint_id=str(endpoint.id))
        db.commit()
        return new_event

    elif result["status"] == "SUCCESS":
        content = result["content"]
        new_event.status_code = result["status_code"]
        new_event.content_length = len(content)
        new_event.etag = result["headers"].get("ETag")
        new_event.last_modified = result["headers"].get("Last-Modified")
        
        # Hash stream
        file_hash = hashlib.sha256(content).hexdigest()
        new_event.content_hash = file_hash
        
        # Check if version exists
        existing_version = db.query(ContentVersion).filter(
            ContentVersion.sha256 == file_hash
        ).first()
        
        if existing_version:
            logger.info("Content hash matched existing version", hash=file_hash)
            db.commit()
            return new_event
            
        # New Version
        doc = db.query(Document).filter(Document.source_id == endpoint.source_id).first()
        if not doc:
            doc = Document(source_id=endpoint.source_id, title="Discovered via Endpoint")
            db.add(doc)
            db.flush()
            
        latest_v = db.query(ContentVersion).filter(ContentVersion.document_id == doc.id).order_by(ContentVersion.version_number.desc()).first()
        v_num = (latest_v.version_number + 1) if latest_v else 1
        
        # Minio path
        storage_path = f"sources/{endpoint.source_id}/documents/{doc.id}/versions/{v_num}/raw"
        StorageService().put(storage_path, content)
        
        new_version = ContentVersion(
            document_id=doc.id,
            version_number=v_num,
            sha256=file_hash,
            byte_size=len(content),
            mime_type=result["headers"].get("Content-Type", "application/octet-stream"),
            storage_path=storage_path
        )
        db.add(new_version)
        db.commit()
        logger.info("New content version created", version_id=str(new_version.id))
        return new_event
        
    else:
        new_event.status_code = result.get("status_code", 500)
        new_event.error_message = result.get("error", "Unknown error")
        db.commit()
        return new_event
