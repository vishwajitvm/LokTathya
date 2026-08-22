from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from core.database import get_db
from models.geography import Geography
from models.representative import Term, Person, Position, Party
from models.election import ElectionResult, Election, Candidate
from models.project import Project
from models.finance import Budget
from models.source import Document, Source
from typing import Dict, Any, List, Optional
import uuid

router = APIRouter(prefix="/api/v1/location", tags=["Location"])

@router.get("/resolve")
def resolve_location(
    latitude: float = Query(...),
    longitude: float = Query(...),
    db: Session = Depends(get_db)
):
    """
    Resolve coordinates to geographic boundaries using PostGIS ST_Contains.
    """
    try:
        # Construct Point geometry using ST_SetSRID and ST_MakePoint
        point = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)
        
        # Query all overlapping geo entities
        stmt = select(Geography).where(func.ST_Contains(Geography.geom, point))
        entities = db.execute(stmt).scalars().all()
        
        if not entities:
            raise HTTPException(status_code=404, detail="NOT_COMPUTABLE")
            
        hierarchy = {}
        for ent in entities:
            hierarchy[ent.type.lower()] = {
                "id": str(ent.id),
                "name": ent.name
            }
            
        return {
            "status": "SUCCESS",
            "hierarchy": hierarchy
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        # If database lacks PostGIS support or spatial query fails
        raise HTTPException(status_code=400, detail="NOT_COMPUTABLE")

@router.get("/{location_id}/profile")
def get_location_profile(location_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Aggregate all context (representatives, elections, finances, projects) for this location.
    """
    geo = db.query(Geography).filter(Geography.id == location_id).first()
    if not geo:
        raise HTTPException(status_code=404, detail="Geography not found")

    # Fetch representatives in this jurisdiction
    terms = db.query(Term).filter(Term.jurisdiction_id == location_id).all()
    representatives = []
    for t in terms:
        p = db.query(Person).filter(Person.id == t.person_id).first()
        pos = db.query(Position).filter(Position.id == t.position_id).first()
        party = db.query(Party).filter(Party.id == t.party_id).first() if t.party_id else None
        
        representatives.append({
            "id": str(p.id) if p else None,
            "name": p.full_name if p else "Unknown",
            "position": pos.title if pos else "Representative",
            "party": party.name if party else "Independent"
        })

    # Fetch election results for this constituency
    results = db.query(ElectionResult).filter(ElectionResult.constituency_id == location_id).all()
    elections_data = []
    for r in results:
        cand = db.query(Candidate).filter(Candidate.id == r.candidate_id).first()
        party = db.query(Party).filter(Party.id == cand.party_id).first() if cand and cand.party_id else None
        elections_data.append({
            "candidate": cand.raw_name if cand else "Unknown",
            "party": party.name if party else "Independent",
            "votes": r.votes,
            "rank": r.rank
        })

    # Return profile data
    return {
        "geography": {
            "id": str(geo.id),
            "name": geo.name,
            "type": geo.type
        },
        "representatives": representatives,
        "elections": elections_data,
        "projects": [], # Empty list instead of stub if no data
        "financial_summary": {
            "status": "INSUFFICIENT_DATA",
            "message": "No financial records linked to this location"
        }
    }
