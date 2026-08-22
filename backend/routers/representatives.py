from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Dict, Any, List
from tracenest import logger
from core.database import get_db
from models.representative import Term, Person, Position, Party

router = APIRouter(prefix="/api/v1/representatives", tags=["Representatives"])

@router.get("/")
def get_representatives(db: Session = Depends(get_db)):
    logger.info("GET /api/v1/representatives – Listing all representatives")
    logger.debug("Database session acquired for representatives query", session_id=str(id(db)))
    # This is a stub for the index, we will return empty if no data.
    logger.info("Representatives listing completed", count=0)
    return []

@router.get("/{rep_id}/terms")
def get_representative_terms(rep_id: str, db: Session = Depends(get_db)):
    logger.info("GET /api/v1/representatives/{rep_id}/terms – Fetching terms", rep_id=rep_id)
    logger.debug("Database session acquired for representative terms", session_id=str(id(db)), rep_id=rep_id)

    # Query database instead of returning fake data
    logger.debug("Executing SQL SELECT on Term table", filter_person_id=rep_id)
    stmt = select(Term).where(Term.person_id == rep_id)
    terms = db.execute(stmt).scalars().all()
    logger.debug("Term query executed", rep_id=rep_id, terms_found=len(terms))

    if not terms:
        logger.info("No terms found for representative", rep_id=rep_id)
        return {"representative_id": rep_id, "terms": []}

    result_terms = []
    for term in terms:
        logger.debug("Processing term record", term_id=str(getattr(term, 'id', 'N/A')), valid_from=str(term.valid_from), valid_until=str(term.valid_until))
        result_terms.append({
            "start_date": term.valid_from,
            "end_date": term.valid_until,
            "position": "Unknown", # Needs join
            "party_at_time": "Unknown", # Needs join
            "jurisdiction": "Unknown" # Needs join
        })

    logger.info("Representative terms returned", rep_id=rep_id, term_count=len(result_terms))
    return {
        "representative_id": rep_id,
        "terms": result_terms
    }
