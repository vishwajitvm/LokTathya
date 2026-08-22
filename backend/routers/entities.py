from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from models.observation import Observation
from models.provenance import CanonicalFact, Claim, Evidence
from models.resolution import EntityResolution
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime, timezone

router = APIRouter(tags=["Entities & Provenance"])

# ── 1. ENTITY ENDPOINTS ───────────────────────────────────────────────

@router.get("/api/v1/entities")
def list_entities(
    target_table: Optional[str] = Query(None),
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(EntityResolution)
    if target_table:
        query = query.filter(EntityResolution.target_table == target_table)
    
    results = query.offset(offset).limit(limit).all()
    return [
        {
            "entity_id": str(r.candidate_id),
            "raw_value": r.raw_value,
            "target_table": r.target_table,
            "status": r.status
        }
        for r in results
    ]

@router.get("/api/v1/entities/{entity_id}")
def get_entity(entity_id: uuid.UUID, db: Session = Depends(get_db)):
    res = db.query(EntityResolution).filter(EntityResolution.candidate_id == entity_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Entity not found")
    return {
        "entity_id": str(res.candidate_id),
        "raw_value": res.raw_value,
        "target_table": res.target_table,
        "status": res.status,
        "confidence": res.confidence
    }

@router.get("/api/v1/entities/{entity_id}/history")
def get_entity_history(entity_id: uuid.UUID, db: Session = Depends(get_db)):
    # Find all canonical facts associated with this entity
    facts = db.query(CanonicalFact).filter(CanonicalFact.entity_id == str(entity_id)).all()
    return [
        {
            "fact_id": str(f.id),
            "attribute_name": f.attribute_name,
            "value": f.value,
            "status": f.status,
            "conflict_status": f.conflict_status,
            "created_at": f.created_at
        }
        for f in facts
    ]


# ── 2. OBSERVATION ENDPOINTS ──────────────────────────────────────────

@router.get("/api/v1/observations")
def list_observations(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    results = db.query(Observation).offset(offset).limit(limit).all()
    return [
        {
            "id": str(o.id),
            "source_id": str(o.source_id),
            "entity_type": o.entity_type,
            "field_name": o.field_name,
            "raw_value": o.raw_value,
            "normalized_value": o.normalized_value,
            "observed_at": o.observed_at,
            "status": o.status
        }
        for o in results
    ]

@router.get("/api/v1/observations/{obs_id}")
def get_observation(obs_id: uuid.UUID, db: Session = Depends(get_db)):
    o = db.query(Observation).filter(Observation.id == obs_id).first()
    if not o:
        raise HTTPException(status_code=404, detail="Observation not found")
    return {
        "id": str(o.id),
        "source_id": str(o.source_id),
        "document_id": str(o.document_id) if o.document_id else None,
        "content_version_id": str(o.content_version_id) if o.content_version_id else None,
        "entity_type": o.entity_type,
        "field_name": o.field_name,
        "raw_value": o.raw_value,
        "normalized_value": o.normalized_value,
        "observed_at": o.observed_at,
        "status": o.status
    }


# ── 3. CANONICAL FACT ENDPOINTS ───────────────────────────────────────

@router.get("/api/v1/canonical-facts")
def list_canonical_facts(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    facts = db.query(CanonicalFact).offset(offset).limit(limit).all()
    return [
        {
            "id": str(f.id),
            "entity_id": f.entity_id,
            "attribute_name": f.attribute_name,
            "value": f.value,
            "status": f.status,
            "conflict_status": f.conflict_status
        }
        for f in facts
    ]

@router.get("/api/v1/canonical-facts/{fact_id}")
def get_canonical_fact(fact_id: uuid.UUID, db: Session = Depends(get_db)):
    f = db.query(CanonicalFact).filter(CanonicalFact.id == fact_id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Canonical fact not found")
    return {
        "id": str(f.id),
        "entity_id": f.entity_id,
        "attribute_name": f.attribute_name,
        "value": f.value,
        "status": f.status,
        "conflict_status": f.conflict_status,
        "created_at": f.created_at
    }


# ── 4. ENTITY RESOLUTION / HUMAN REVIEW ENDPOINTS ─────────────────────

@router.get("/api/v1/entity-resolution/reviews")
def list_pending_reviews(db: Session = Depends(get_db)):
    reviews = db.query(EntityResolution).filter(EntityResolution.status == "HUMAN_REVIEW").all()
    return [
        {
            "id": str(r.id),
            "raw_value": r.raw_value,
            "target_table": r.target_table,
            "confidence": r.confidence,
            "status": r.status
        }
        for r in reviews
    ]

@router.post("/api/v1/entity-resolution/reviews/{review_id}/resolve")
def resolve_review_item(review_id: uuid.UUID, matched_entity_id: uuid.UUID, db: Session = Depends(get_db)):
    r = db.query(EntityResolution).filter(EntityResolution.id == review_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Review record not found")
        
    r.candidate_id = matched_entity_id
    r.status = "CONFIRMED"
    r.resolved_at = datetime.now(timezone.utc)
    db.commit()
    return {"status": "SUCCESS", "entity_id": str(matched_entity_id)}


# ── 5. PROVENANCE GRAPH ENDPOINT ──────────────────────────────────────

@router.get("/api/v1/provenance/{fact_id}")
def get_fact_provenance(fact_id: uuid.UUID, db: Session = Depends(get_db)):
    # Trace CanonicalFact -> Claim -> Evidence
    fact = db.query(CanonicalFact).filter(CanonicalFact.id == fact_id).first()
    if not fact:
        raise HTTPException(status_code=404, detail="Fact not found")
        
    claims = db.query(Claim).filter(Claim.canonical_fact_id == fact_id).all()
    
    trace = []
    for c in claims:
        evidences = db.query(Evidence).filter(Evidence.claim_id == c.id).all()
        trace.append({
            "claim_id": str(c.id),
            "description": c.description,
            "status": c.status,
            "evidence": [
                {
                    "evidence_id": str(e.id),
                    "source_id": str(e.source_id),
                    "document_id": str(e.document_id) if e.document_id else None,
                    "content_version_id": str(e.content_version_id) if e.content_version_id else None
                }
                for e in evidences
            ]
        })
        
    return {
        "fact_id": str(fact.id),
        "attribute_name": fact.attribute_name,
        "value": fact.value,
        "provenance_chain": trace
    }
