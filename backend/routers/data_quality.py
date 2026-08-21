from fastapi import APIRouter
from typing import List, Dict, Any
from data_quality.reconciliation import ReconciliationEngine

router = APIRouter(prefix="/api/v1/data-quality", tags=["Data Quality"])

@router.get("/conflicts", response_model=Dict[str, Any])
def list_conflicts(limit: int = 50, offset: int = 0):
    # Dummy mock of unresolved conflicts
    return {
        "data": [
            {
                "entity_id": "proj-123",
                "field": "allocated_amount",
                "status": "CONFLICTING",
                "observations": [
                    {"source_id": "SRC-A", "value": 100000},
                    {"source_id": "SRC-B", "value": 120000}
                ],
                "requires_review": True
            }
        ],
        "meta": {"limit": limit, "offset": offset, "has_more": False}
    }
