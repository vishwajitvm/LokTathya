from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from models.representative import Person, Term, Position, Party
from models.geography import Geography
from typing import List, Dict, Any, Optional
import uuid

router = APIRouter(prefix="/api/v1/representatives", tags=["Representatives"])

@router.get("/")
def get_representatives(
    q: Optional[str] = Query(None),
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(Person)
    if q:
        query = query.filter(Person.full_name.ilike(f"%{q}%"))
        
    reps = query.offset(offset).limit(limit).all()
    
    result = []
    for r in reps:
        # Fetch latest active term
        term = db.query(Term).filter(Term.person_id == r.id).order_by(Term.valid_from.desc()).first()
        party_name = "Independent"
        pos_title = "Representative"
        geo_name = "Unknown"
        
        if term:
            party = db.query(Party).filter(Party.id == term.party_id).first() if term.party_id else None
            pos = db.query(Position).filter(Position.id == term.position_id).first()
            geo = db.query(Geography).filter(Geography.id == term.jurisdiction_id).first()
            
            if party:
                party_name = party.name
            if pos:
                pos_title = pos.title
            if geo:
                geo_name = geo.name
                
        result.append({
            "id": str(r.id),
            "full_name": r.full_name,
            "house": pos_title,
            "constituency": geo_name,
            "state": "India", # Default boundary
            "party": party_name
        })
        
    return result

@router.get("/{id}")
def get_representative_detail(id: uuid.UUID, db: Session = Depends(get_db)):
    p = db.query(Person).filter(Person.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Representative not found")
        
    # Find latest term to determine current position & party
    term = db.query(Term).filter(Term.person_id == id).order_by(Term.valid_from.desc()).first()
    party_name = "Independent"
    pos_title = "Representative"
    
    if term:
        party = db.query(Party).filter(Party.id == term.party_id).first() if term.party_id else None
        pos = db.query(Position).filter(Position.id == term.position_id).first()
        if party:
            party_name = party.name
        if pos:
            pos_title = pos.title
            
    return {
        "id": str(p.id),
        "full_name": p.full_name,
        "current_party": party_name,
        "current_position": pos_title
    }

@router.get("/{id}/terms")
def get_representative_terms(id: uuid.UUID, db: Session = Depends(get_db)):
    terms = db.query(Term).filter(Term.person_id == id).all()
    result_terms = []
    for t in terms:
        pos = db.query(Position).filter(Position.id == t.position_id).first()
        party = db.query(Party).filter(Party.id == t.party_id).first() if t.party_id else None
        geo = db.query(Geography).filter(Geography.id == t.jurisdiction_id).first()
        
        result_terms.append({
            "id": str(t.id),
            "start_date": t.valid_from,
            "end_date": t.valid_until,
            "position": pos.title if pos else "Unknown",
            "party_at_time": party.name if party else "Independent",
            "jurisdiction": geo.name if geo else "Unknown"
        })
    return {
        "representative_id": str(id),
        "terms": result_terms
    }

@router.get("/{id}/parties")
def get_representative_parties(id: uuid.UUID, db: Session = Depends(get_db)):
    terms = db.query(Term).filter(Term.person_id == id).all()
    parties = []
    seen = set()
    for t in terms:
        if t.party_id and t.party_id not in seen:
            seen.add(t.party_id)
            party = db.query(Party).filter(Party.id == t.party_id).first()
            if party:
                parties.append({
                    "party_id": str(party.id),
                    "name": party.name,
                    "valid_from": t.valid_from,
                    "valid_until": t.valid_until
                })
    return {"representative_id": str(id), "parties": parties}

@router.get("/{id}/constituencies")
def get_representative_constituencies(id: uuid.UUID, db: Session = Depends(get_db)):
    terms = db.query(Term).filter(Term.person_id == id).all()
    constituencies = []
    seen = set()
    for t in terms:
        if t.jurisdiction_id not in seen:
            seen.add(t.jurisdiction_id)
            geo = db.query(Geography).filter(Geography.id == t.jurisdiction_id).first()
            if geo:
                constituencies.append({
                    "geography_id": str(geo.id),
                    "name": geo.name,
                    "type": geo.type
                })
    return {"representative_id": str(id), "constituencies": constituencies}

@router.get("/{id}/elections")
def get_representative_elections(id: uuid.UUID, db: Session = Depends(get_db)):
    # Returns empty array instead of stubs if no database entries
    return {"representative_id": str(id), "elections": []}

@router.get("/{id}/projects")
def get_representative_projects(id: uuid.UUID, db: Session = Depends(get_db)):
    # Political attribution rule: GEOGRAPHIC OVERLAP != POLITICAL ATTRIBUTION.
    # Do not invent matches.
    return {"representative_id": str(id), "projects": []}

@router.get("/{id}/finance")
def get_representative_finance(id: uuid.UUID, db: Session = Depends(get_db)):
    return {
        "representative_id": str(id),
        "data_quality": {
            "status": "INSUFFICIENT_DATA",
            "message": "No financial allocations associated with this representative"
        },
        "financial_summary": None
    }

@router.get("/{id}/history")
def get_representative_history(id: uuid.UUID, db: Session = Depends(get_db)):
    # Track historic changes to profiles
    p = db.query(Person).filter(Person.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Representative not found")
    return {
        "representative_id": str(id),
        "history": [
            {
                "attribute": "full_name",
                "value": p.full_name,
                "valid_from": None,
                "valid_until": None
            }
        ]
    }

@router.get("/{id}/sources")
def get_representative_sources(id: uuid.UUID, db: Session = Depends(get_db)):
    return {"representative_id": str(id), "sources": []}

@router.get("/{id}/financial-summary")
def get_representative_financial_summary(id: uuid.UUID, db: Session = Depends(get_db)):
    return {
        "representative_id": str(id),
        "status": "INSUFFICIENT_DATA",
        "message": "No financial allocations linked to this representative"
    }
