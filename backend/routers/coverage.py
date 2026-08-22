from fastapi import APIRouter
from typing import Dict, Any
from tracenest import logger
from source_registry.coverage import CoverageEngine
from source_registry.health import SourceHealthTracker

router = APIRouter(prefix="/api/v1/coverage", tags=["Source Coverage"])

@router.get("/{jurisdiction_id}")
def get_jurisdiction_coverage(jurisdiction_id: str, category: str = None):
    effective_category = category or "elections"
    logger.info("GET /api/v1/coverage/{jurisdiction_id} – Calculating source coverage", jurisdiction_id=jurisdiction_id, category=effective_category)
    logger.debug("Delegating to CoverageEngine.calculate_coverage", jurisdiction_id=jurisdiction_id, category=effective_category)
    try:
        result = CoverageEngine.calculate_coverage(jurisdiction_id, effective_category)
        logger.info("Coverage calculation completed", jurisdiction_id=jurisdiction_id, category=effective_category)
        return result
    except Exception as e:
        logger.error("Coverage calculation FAILED", jurisdiction_id=jurisdiction_id, category=effective_category, error=str(e))
        raise

@router.get("/health/{source_id}")
def get_source_health(source_id: str):
    logger.info("GET /api/v1/coverage/health/{source_id} – Pinging source health", source_id=source_id)
    logger.debug("Delegating to SourceHealthTracker.ping_source", source_id=source_id, endpoint="https://mock.gov.in/api")
    try:
        result = SourceHealthTracker.ping_source(source_id, "https://mock.gov.in/api")
        logger.info("Source health check completed", source_id=source_id, status=str(result.get("status", "unknown")) if isinstance(result, dict) else "ok")
        return result
    except Exception as e:
        logger.error("Source health check FAILED", source_id=source_id, error=str(e))
        raise
