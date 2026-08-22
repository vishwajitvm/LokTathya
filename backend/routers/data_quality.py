from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.provenance import CanonicalFact
from typing import List, Dict, Any
from tracenest import logger

router = APIRouter(prefix="/api/v1/data-quality", tags=["Data Quality"])

@router.get("/conflicts", response_model=Dict[str, Any])
def list_conflicts(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    logger.info("GET /api/v1/data-quality/conflicts – Listing data quality conflicts", limit=limit, offset=offset)
    
    conflicts = db.query(CanonicalFact).filter(
        CanonicalFact.conflict_status == "CONFLICTING"
    ).offset(offset).limit(limit).all()
    
    result = {
        "data": [
            {
                "id": str(c.id),
                "entity_id": c.entity_id,
                "attribute_name": c.attribute_name,
                "value": c.value,
                "status": c.status
            }
            for c in conflicts
        ],
        "meta": {"limit": limit, "offset": offset, "has_more": len(conflicts) == limit}
    }
    return result
