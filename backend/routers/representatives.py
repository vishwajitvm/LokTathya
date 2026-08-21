from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Dict, Any, List
from core.database import get_db
from models.representative import Term, Person, Position, Party

router = APIRouter(prefix="/api/v1/representatives", tags=["Representatives"])

@router.get("/")
def get_representatives(db: Session = Depends(get_db)):
    # This is a stub for the index, we will return empty if no data.
    return []

@router.get("/{rep_id}/terms")
def get_representative_terms(rep_id: str, db: Session = Depends(get_db)):
    # Query database instead of returning fake data
    stmt = select(Term).where(Term.person_id == rep_id)
    terms = db.execute(stmt).scalars().all()
    
    if not terms:
        return {"representative_id": rep_id, "terms": []}
        
    result_terms = []
    for term in terms:
        result_terms.append({
            "start_date": term.valid_from,
            "end_date": term.valid_until,
            "position": "Unknown", # Needs join
            "party_at_time": "Unknown", # Needs join
            "jurisdiction": "Unknown" # Needs join
        })

    return {
        "representative_id": rep_id,
        "terms": result_terms
    }
