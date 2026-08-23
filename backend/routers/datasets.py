from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from core.database import get_db
from models.dataset import Dataset, DatasetVersion, DatasetSchema, DatasetField, DatasetQualityProfile
import uuid
from typing import Optional, List

router = APIRouter(prefix="/api/v1/datasets", tags=["Datasets"])

@router.get("/")
def list_datasets(
    source_id: Optional[uuid.UUID] = Query(None),
    q: Optional[str] = Query(None),
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List and search available datasets."""
    query = db.query(Dataset)
    if source_id:
        query = query.filter(Dataset.source_id == source_id)
    if q:
        query = query.filter(Dataset.name.ilike(f"%{q}%"))
        
    datasets = query.order_by(Dataset.created_at.desc()).offset(offset).limit(limit).all()
    return [
        {
            "id": str(d.id),
            "source_id": str(d.source_id),
            "name": d.name,
            "description": d.description,
            "status": d.status,
            "created_at": d.created_at
        }
        for d in datasets
    ]

@router.get("/{id}")
def get_dataset(id: uuid.UUID, db: Session = Depends(get_db)):
    """Get dataset identity details."""
    d = db.query(Dataset).filter(Dataset.id == id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    return {
        "id": str(d.id),
        "source_id": str(d.source_id),
        "name": d.name,
        "description": d.description,
        "status": d.status,
        "created_at": d.created_at
    }

@router.get("/{id}/versions")
def get_dataset_versions(id: uuid.UUID, db: Session = Depends(get_db)):
    """List all immutable versions of a dataset."""
    d = db.query(Dataset).filter(Dataset.id == id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    versions = db.query(DatasetVersion).filter(
        DatasetVersion.dataset_id == id
    ).order_by(DatasetVersion.valid_from.desc()).all()
    
    return [
        {
            "id": str(v.id),
            "content_hash": v.content_hash,
            "valid_from": v.valid_from,
            "valid_until": v.valid_until,
            "change_classification": v.change_classification
        }
        for v in versions
    ]

@router.get("/{id}/schema")
def get_dataset_schema(id: uuid.UUID, version_id: Optional[uuid.UUID] = Query(None), db: Session = Depends(get_db)):
    """Get the inferred schema and semantic field mappings."""
    # Find active version
    if version_id:
        v = db.query(DatasetVersion).filter(DatasetVersion.id == version_id, DatasetVersion.dataset_id == id).first()
    else:
        v = db.query(DatasetVersion).filter(DatasetVersion.dataset_id == id).order_by(DatasetVersion.valid_from.desc()).first()
        
    if not v:
        raise HTTPException(status_code=404, detail="Dataset version not found")
        
    schema = db.query(DatasetSchema).filter(DatasetSchema.dataset_version_id == v.id).first()
    if not schema:
        return {"columns": [], "fields": []}
        
    fields = db.query(DatasetField).filter(DatasetField.dataset_schema_id == schema.id).all()
    
    return {
        "version_id": str(v.id),
        "inferred_schema": schema.inferred_schema,
        "semantic_fields": [
            {
                "id": str(f.id),
                "original_name": f.original_name,
                "semantic_type": f.semantic_type,
                "confidence": f.confidence,
                "status": f.status
            }
            for f in fields
        ]
    }

@router.get("/{id}/quality")
def get_dataset_quality(id: uuid.UUID, version_id: Optional[uuid.UUID] = Query(None), db: Session = Depends(get_db)):
    """Get the quality profile for a dataset version."""
    if version_id:
        v = db.query(DatasetVersion).filter(DatasetVersion.id == version_id, DatasetVersion.dataset_id == id).first()
    else:
        v = db.query(DatasetVersion).filter(DatasetVersion.dataset_id == id).order_by(DatasetVersion.valid_from.desc()).first()
        
    if not v:
        raise HTTPException(status_code=404, detail="Dataset version not found")
        
    q = db.query(DatasetQualityProfile).filter(DatasetQualityProfile.dataset_version_id == v.id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Quality profile not found for this version")
        
    return {
        "version_id": str(v.id),
        "row_count": q.row_count,
        "column_count": q.column_count,
        "null_ratio": q.null_ratio,
        "duplicate_row_ratio": q.duplicate_row_ratio,
        "profiled_at": q.profiled_at
    }

@router.get("/{id}/changes")
def get_dataset_changes(id: uuid.UUID, db: Session = Depends(get_db)):
    """Compare latest version against previous version."""
    versions = db.query(DatasetVersion).filter(
        DatasetVersion.dataset_id == id
    ).order_by(DatasetVersion.valid_from.desc()).limit(2).all()
    
    if len(versions) < 2:
        return {"status": "INSUFFICIENT_HISTORY", "message": "At least 2 versions required to diff."}
        
    latest = versions[0]
    previous = versions[1]
    
    # We can fetch schemas and compare columns
    schema_latest = db.query(DatasetSchema).filter(DatasetSchema.dataset_version_id == latest.id).first()
    schema_prev = db.query(DatasetSchema).filter(DatasetSchema.dataset_version_id == previous.id).first()
    
    cols_latest = set(c["name"] for c in schema_latest.inferred_schema.get("columns", [])) if schema_latest else set()
    cols_prev = set(c["name"] for c in schema_prev.inferred_schema.get("columns", [])) if schema_prev else set()
    
    added = cols_latest - cols_prev
    removed = cols_prev - cols_latest
    
    return {
        "dataset_id": str(id),
        "latest_version_id": str(latest.id),
        "previous_version_id": str(previous.id),
        "content_changed": latest.content_hash != previous.content_hash,
        "schema_drift": {
            "columns_added": list(added),
            "columns_removed": list(removed)
        }
    }
