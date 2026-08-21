from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter(prefix="/api/v1/representatives", tags=["Representatives"])

@router.get("/{rep_id}/terms")
def get_representative_terms(rep_id: str):
    return {
        "representative_id": rep_id,
        "terms": [
            {
                "start_date": "2019-05-23",
                "end_date": "2024-05-04",
                "position": "MP",
                "party_at_time": "Party A",
                "jurisdiction": "Constituency X"
            }
        ]
    }
