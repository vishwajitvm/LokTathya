from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from models.source import Document, ContentVersion
import uuid
from typing import Optional

router = APIRouter(prefix="/api/v1/documents", tags=["Documents"])

@router.get("/{document_id}")
def get_document(document_id: uuid.UUID, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {
        "id": str(doc.id),
        "source_id": str(doc.source_id) if doc.source_id else None,
        "document_type": doc.document_type,
        "title": doc.title,
        "publication_date": doc.publication_date,
        "canonical_url": doc.canonical_url,
        "status": doc.status,
        "created_at": doc.created_at
    }

@router.get("/{document_id}/versions")
def get_document_versions(document_id: uuid.UUID, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    versions = db.query(ContentVersion).filter(ContentVersion.document_id == document_id).order_by(ContentVersion.version_number.desc()).all()
    
    return {
        "document_id": str(document_id),
        "versions": [
            {
                "id": str(v.id),
                "version_number": v.version_number,
                "sha256": v.sha256,
                "byte_size": v.byte_size,
                "mime_type": v.mime_type,
                "storage_path": v.storage_path,
                "retrieved_at": v.retrieved_at
            }
            for v in versions
        ]
    }
