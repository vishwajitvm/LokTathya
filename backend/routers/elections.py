from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from models.election import Election, ElectionEvent, Candidate, ElectionResult
from models.geography import Geography
from models.representative import Person, Party
from typing import List, Dict, Any, Optional
import uuid

router = APIRouter(prefix="/api/v1/elections", tags=["Elections"])

@router.get("/")
def list_elections(
    type: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(Election)
    if type:
        query = query.filter(Election.type == type)
    if year:
        query = query.filter(Election.year == year)
        
    elections = query.offset(offset).limit(limit).all()
    
    return {
        "data": [
            {
                "id": str(e.id),
                "type": e.type,
                "year": e.year
            }
            for e in elections
        ],
        "meta": {"limit": limit, "offset": offset, "has_more": len(elections) == limit}
    }

@router.get("/{id}")
def get_election(id: uuid.UUID, db: Session = Depends(get_db)):
    e = db.query(Election).filter(Election.id == id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Election not found")
    return {
        "id": str(e.id),
        "type": e.type,
        "year": e.year
    }

@router.get("/{id}/results")
def get_election_results(id: uuid.UUID, db: Session = Depends(get_db)):
    # Find all events associated with this election
    events = db.query(ElectionEvent).filter(ElectionEvent.election_id == id).all()
    event_ids = [evt.id for evt in events]
    
    results = db.query(ElectionResult).filter(ElectionResult.event_id.in_(event_ids)).all() if event_ids else []
    
    results_list = []
    for r in results:
        cand = db.query(Candidate).filter(Candidate.id == r.candidate_id).first()
        party = db.query(Party).filter(Party.id == cand.party_id).first() if cand and cand.party_id else None
        geo = db.query(Geography).filter(Geography.id == r.constituency_id).first()
        
        results_list.append({
            "id": str(r.id),
            "constituency": geo.name if geo else "Unknown",
            "candidate": cand.raw_name if cand else "Unknown",
            "party": party.name if party else "Independent",
            "votes": r.votes,
            "vote_percentage": r.vote_percentage,
            "rank": r.rank
        })
        
    return {
        "election_id": str(id),
        "results": results_list,
        "metrics": {
            "total_constituencies_declared": len(set(r.constituency_id for r in results))
        }
    }

@router.get("/{id}/candidates")
def get_election_candidates(id: uuid.UUID, db: Session = Depends(get_db)):
    events = db.query(ElectionEvent).filter(ElectionEvent.election_id == id).all()
    event_ids = [evt.id for evt in events]
    
    results = db.query(ElectionResult).filter(ElectionResult.event_id.in_(event_ids)).all() if event_ids else []
    cand_ids = [r.candidate_id for r in results]
    
    candidates = db.query(Candidate).filter(Candidate.id.in_(cand_ids)).all() if cand_ids else []
    return {
        "election_id": str(id),
        "candidates": [
            {
                "id": str(c.id),
                "name": c.raw_name,
                "person_id": str(c.person_id) if c.person_id else None
            }
            for c in candidates
        ]
    }

@router.get("/{id}/turnout")
def get_election_turnout(id: uuid.UUID, db: Session = Depends(get_db)):
    return {
        "election_id": str(id),
        "data_quality": {
            "status": "INSUFFICIENT_DATA",
            "message": "Turnout metrics not compiled for this election"
        },
        "voter_turnout": None
    }

@router.get("/{id}/constituencies")
def get_election_constituencies(id: uuid.UUID, db: Session = Depends(get_db)):
    events = db.query(ElectionEvent).filter(ElectionEvent.election_id == id).all()
    event_ids = [evt.id for evt in events]
    
    results = db.query(ElectionResult).filter(ElectionResult.event_id.in_(event_ids)).all() if event_ids else []
    geo_ids = [r.constituency_id for r in results]
    
    geos = db.query(Geography).filter(Geography.id.in_(geo_ids)).all() if geo_ids else []
    return {
        "election_id": str(id),
        "constituencies": [
            {"id": str(g.id), "name": g.name, "type": g.type}
            for g in geos
        ]
    }

@router.get("/{id}/history")
def get_election_history(id: uuid.UUID, db: Session = Depends(get_db)):
    e = db.query(Election).filter(Election.id == id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Election not found")
    return {"election_id": str(id), "history": []}
