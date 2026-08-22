from fastapi import APIRouter
from typing import Dict, Any
from tracenest import logger
from geography.historical import HistoricalGeographyEngine, DelimitationManager

router = APIRouter(prefix="/api/v1/geographies", tags=["Historical Geography"])

@router.get("/history")
def get_geographic_history():
    logger.info("GET /api/v1/geographies/history – Fetching geographic history timeline")
    logger.debug("Geographic history endpoint invoked (stub)")
    logger.info("Geographic history returned", status="ok")
    return {"status": "ok"}

@router.get("/comparability")
def check_comparability(geo_a: str, geo_b: str):
    logger.info("GET /api/v1/geographies/comparability – Checking geographic comparability", geo_a=geo_a, geo_b=geo_b)
    logger.debug("Delegating to HistoricalGeographyEngine.evaluate_comparability", geo_a=geo_a, geo_b=geo_b)
    try:
        result = HistoricalGeographyEngine.evaluate_comparability(geo_a, geo_b)
        logger.info("Comparability evaluation completed", geo_a=geo_a, geo_b=geo_b)
        return result
    except Exception as e:
        logger.error("Comparability evaluation FAILED", geo_a=geo_a, geo_b=geo_b, error=str(e))
        raise
