from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter(prefix="/api/v1/data-quality", tags=["Data Quality"])

@router.get("/conflicts", response_model=Dict[str, Any])
def list_conflicts(limit: int = 50, offset: int = 0):
    # No mock data allowed
    return {
        "data": [],
        "meta": {"limit": limit, "offset": offset, "has_more": False}
    }
