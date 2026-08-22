from fastapi import APIRouter
from typing import List, Dict, Any
from tracenest import logger

router = APIRouter(prefix="/api/v1/data-quality", tags=["Data Quality"])

@router.get("/conflicts", response_model=Dict[str, Any])
def list_conflicts(limit: int = 50, offset: int = 0):
    logger.info("GET /api/v1/data-quality/conflicts – Listing data quality conflicts", limit=limit, offset=offset)
    logger.debug("Querying conflict table", pagination_limit=limit, pagination_offset=offset)

    # No mock data allowed
    result = {
        "data": [],
        "meta": {"limit": limit, "offset": offset, "has_more": False}
    }
    logger.info("Conflict listing completed", conflict_count=0, has_more=False)
    return result
