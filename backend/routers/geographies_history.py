from fastapi import APIRouter
from typing import Dict, Any
from geography.historical import HistoricalGeographyEngine, DelimitationManager

router = APIRouter(prefix="/api/v1/geographies", tags=["Historical Geography"])

@router.get("/history")
def get_geographic_history():
    return {"status": "ok"}

@router.get("/comparability")
def check_comparability(geo_a: str, geo_b: str):
    return HistoricalGeographyEngine.evaluate_comparability(geo_a, geo_b)
