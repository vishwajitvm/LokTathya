from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from models.source import Document, ContentVersion, Source
from models.provenance import Evidence, Claim
from typing import List, Dict, Any, Optional
import uuid

router = APIRouter(prefix="/api/v1/documents", tags=["Documents"])

@router.get("/")
def list_documents(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    docs = db.query(Document).offset(offset).limit(limit).all()
    return {
        "data": [
            {
                "id": str(d.id),
                "source_id": str(d.source_id) if d.source_id else None,
                "document_type": d.document_type,
                "title": d.title,
                "publication_date": d.publication_date,
                "status": d.status
            }
            for d in docs
        ],
        "meta": {"limit": limit, "offset": offset, "has_more": len(docs) == limit}
    }

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

@router.get("/{document_id}/diff")
def get_document_diff(document_id: uuid.UUID, v1: int, v2: int, db: Session = Depends(get_db)):
    version_a = db.query(ContentVersion).filter(ContentVersion.document_id == document_id, ContentVersion.version_number == v1).first()
    version_b = db.query(ContentVersion).filter(ContentVersion.document_id == document_id, ContentVersion.version_number == v2).first()
    
    if not version_a or not version_b:
        raise HTTPException(status_code=404, detail="One or both versions not found")
        
    # In real pipeline, load and run diff
    from ingestion.diff_engine import DocumentDiffEngine
    engine = DocumentDiffEngine()
    
    diff_res = engine.diff_text(
        f"Simulated document version {v1} content",
        f"Simulated document version {v2} content"
    )
    
    return {
        "document_id": str(document_id),
        "v1": v1,
        "v2": v2,
        "diff": diff_res
    }

@router.get("/{document_id}/provenance")
def get_document_provenance(document_id: uuid.UUID, db: Session = Depends(get_db)):
    evidences = db.query(Evidence).filter(Evidence.document_id == document_id).all()
    provenance_list = []
    for ev in evidences:
        claim = db.query(Claim).filter(Claim.id == ev.claim_id).first()
        if claim:
            provenance_list.append({
                "claim_id": str(claim.id),
                "description": claim.description,
                "level": claim.claim_level,
                "status": claim.status
            })
    return {
        "document_id": str(document_id),
        "extracted_provenance": provenance_list
    }

@router.get("/{document_id}/sources")
def get_document_sources(document_id: uuid.UUID, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    src = db.query(Source).filter(Source.id == doc.source_id).first() if doc.source_id else None
    return {
        "document_id": str(document_id),
        "sources": [
            {
                "id": str(src.id),
                "name": src.name,
                "status": src.status
            }
            if src else {}
        ]
    }
