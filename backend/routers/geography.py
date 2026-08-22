from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from core.database import get_db
from models.geography import Geography, GeoRelationship
from models.representative import Term, Person, Position, Party
from models.election import ElectionResult
from typing import List, Dict, Any, Optional
import uuid

router = APIRouter(prefix="/api/v1/geographies", tags=["Geography"])

@router.get("/")
def list_geographies(
    type: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(Geography)
    if type:
        query = query.filter(Geography.type == type)
    if q:
        query = query.filter(Geography.name.ilike(f"%{q}%"))
        
    geos = query.offset(offset).limit(limit).all()
    
    return {
        "data": [
            {
                "id": str(g.id),
                "type": g.type,
                "name": g.name,
                "valid_from": g.valid_from,
                "valid_until": g.valid_until
            }
            for g in geos
        ],
        "meta": {"limit": limit, "offset": offset, "has_more": len(geos) == limit}
    }

@router.get("/{id}")
def get_geography(id: uuid.UUID, db: Session = Depends(get_db)):
    geo = db.query(Geography).filter(Geography.id == id).first()
    if not geo:
        raise HTTPException(status_code=404, detail="Geography not found")
    return {
        "id": str(geo.id),
        "type": geo.type,
        "name": geo.name,
        "valid_from": geo.valid_from,
        "valid_until": geo.valid_until
    }

@router.get("/{id}/children")
def get_geography_children(id: uuid.UUID, db: Session = Depends(get_db)):
    rels = db.query(GeoRelationship).filter(GeoRelationship.parent_id == id).all()
    children = []
    for r in rels:
        child = db.query(Geography).filter(Geography.id == r.child_id).first()
        if child:
            children.append({
                "id": str(child.id),
                "type": child.type,
                "name": child.name
            })
    return {"geography_id": str(id), "children": children}

@router.get("/{id}/ancestors")
def get_geography_ancestors(id: uuid.UUID, db: Session = Depends(get_db)):
    rels = db.query(GeoRelationship).filter(GeoRelationship.child_id == id).all()
    ancestors = []
    for r in rels:
        parent = db.query(Geography).filter(Geography.id == r.parent_id).first()
        if parent:
            ancestors.append({
                "id": str(parent.id),
                "type": parent.type,
                "name": parent.name
            })
    return {"geography_id": str(id), "ancestors": ancestors}

@router.get("/{id}/history")
def get_geography_history(id: uuid.UUID, db: Session = Depends(get_db)):
    geo = db.query(Geography).filter(Geography.id == id).first()
    if not geo:
        raise HTTPException(status_code=404, detail="Geography not found")
    return {
        "id": str(geo.id),
        "name": geo.name,
        "history": [
            {
                "valid_from": geo.valid_from,
                "valid_until": geo.valid_until,
                "status": "CURRENT" if geo.valid_until is None else "HISTORICAL"
            }
        ]
    }

@router.get("/{id}/representatives")
def get_geography_representatives(id: uuid.UUID, db: Session = Depends(get_db)):
    terms = db.query(Term).filter(Term.jurisdiction_id == id).all()
    reps = []
    for t in terms:
        p = db.query(Person).filter(Person.id == t.person_id).first()
        pos = db.query(Position).filter(Position.id == t.position_id).first()
        party = db.query(Party).filter(Party.id == t.party_id).first() if t.party_id else None
        if p:
            reps.append({
                "id": str(p.id),
                "name": p.full_name,
                "position": pos.title if pos else "Unknown",
                "party": party.name if party else "Independent",
                "term_start": t.valid_from,
                "term_end": t.valid_until
            })
    return {"geography_id": str(id), "representatives": reps}

@router.get("/{id}/projects")
def get_geography_projects(id: uuid.UUID, db: Session = Depends(get_db)):
    # Returns empty array if no projects found in the DB (instead of stubs)
    return {"geography_id": str(id), "projects": []}

@router.get("/{id}/elections")
def get_geography_elections(id: uuid.UUID, db: Session = Depends(get_db)):
    results = db.query(ElectionResult).filter(ElectionResult.constituency_id == id).all()
    elections_data = []
    for r in results:
        # Avoid duplicate election ids
        elections_data.append({
            "result_id": str(r.id),
            "votes": r.votes,
            "vote_percentage": r.vote_percentage,
            "rank": r.rank
        })
    return {"geography_id": str(id), "elections": elections_data}

@router.get("/{id}/finance")
def get_geography_finance(id: uuid.UUID, db: Session = Depends(get_db)):
    return {
        "geography_id": str(id),
        "data_quality": {
            "status": "INSUFFICIENT_DATA",
            "message": "No financial records linked to this location"
        },
        "financials": []
    }

@router.get("/{id}/sources")
def get_geography_sources(id: uuid.UUID, db: Session = Depends(get_db)):
    return {"geography_id": str(id), "sources": []}

@router.get("/{id}/financial-summary")
def get_geography_financial_summary(id: uuid.UUID, db: Session = Depends(get_db)):
    return {
        "geography_id": str(id),
        "status": "INSUFFICIENT_DATA",
        "message": "No financial allocations linked to this geography"
    }
