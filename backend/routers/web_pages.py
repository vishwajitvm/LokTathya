from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from models.web_page import WebPage, WebPageVersion, ExtractedTable
from models.source import Source
import uuid
from typing import List, Dict, Any

router = APIRouter(prefix="/api/v1/web-pages", tags=["Web Pages"])

@router.get("/{page_id}")
def get_web_page(page_id: uuid.UUID, db: Session = Depends(get_db)):
    page = db.query(WebPage).filter(WebPage.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Web page not found")
    return {
        "id": str(page.id),
        "source_id": str(page.source_id),
        "canonical_url": page.canonical_url,
        "current_url": page.current_url,
        "title": page.title,
        "description": page.description,
        "language": page.language,
        "page_type": page.page_type,
        "status_code": page.status_code,
        "first_seen_at": page.first_seen_at,
        "last_seen_at": page.last_seen_at
    }

@router.get("/{page_id}/versions")
def get_web_page_versions(page_id: uuid.UUID, db: Session = Depends(get_db)):
    page = db.query(WebPage).filter(WebPage.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Web page not found")
        
    versions = db.query(WebPageVersion).filter(WebPageVersion.page_id == page_id).order_by(WebPageVersion.version_number.desc()).all()
    
    return {
        "page_id": str(page_id),
        "versions": [
            {
                "id": str(v.id),
                "version_number": v.version_number,
                "content_hash": v.content_hash,
                "raw_html_hash": v.raw_html_hash,
                "change_type": v.change_type,
                "retrieved_at": v.retrieved_at,
                "storage_path": v.storage_path
            }
            for v in versions
        ]
    }

@router.get("/{page_id}/links")
def get_web_page_links(page_id: uuid.UUID, db: Session = Depends(get_db)):
    # Get links discovered on the latest version of this page
    latest_version = db.query(WebPageVersion).filter(WebPageVersion.page_id == page_id).order_by(WebPageVersion.version_number.desc()).first()
    if not latest_version:
        raise HTTPException(status_code=404, detail="No versions found for this web page")
        
    # We would read links from metadata or extracted links table.
    # Since they are stored in extracted_metadata["links"] or similar:
    links = latest_version.extracted_metadata.get("links", [])
    return {
        "page_id": str(page_id),
        "version_id": str(latest_version.id),
        "links": links
    }

@router.get("/{page_id}/diff")
def get_web_page_diff(page_id: uuid.UUID, v1: int, v2: int, db: Session = Depends(get_db)):
    # Retrieve two versions and diff them
    version_a = db.query(WebPageVersion).filter(WebPageVersion.page_id == page_id, WebPageVersion.version_number == v1).first()
    version_b = db.query(WebPageVersion).filter(WebPageVersion.page_id == page_id, WebPageVersion.version_number == v2).first()
    
    if not version_a or not version_b:
        raise HTTPException(status_code=404, detail="One or both versions not found")
        
    # In real pipeline, we load normalized text and run diff
    from ingestion.diff_engine import DocumentDiffEngine
    engine = DocumentDiffEngine()
    
    # Simple simulated text content for test or retrieved text content
    text_a = f"Simulated text for version {v1}"
    text_b = f"Simulated text for version {v2}"
    
    diff_res = engine.diff_text(text_a, text_b)
    
    return {
        "page_id": str(page_id),
        "v1": v1,
        "v2": v2,
        "diff": diff_res
    }
