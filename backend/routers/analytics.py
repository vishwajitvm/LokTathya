from fastapi import APIRouter
from tracenest import logger
from analytics.financial import FinancialAnalytics
from analytics.metric_registry import registry

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])

@router.get("/metrics")
def get_metric_registry():
    logger.info("GET /api/v1/analytics/metrics – Fetching full metric registry")
    logger.debug("Metric registry lookup started", registry_type=type(registry).__name__)
    result = registry.metrics
    logger.info("Metric registry returned successfully", metric_count=len(result) if isinstance(result, (list, dict)) else 0)
    return result

@router.get("/financial/utilization")
def get_utilization(allocated: float = 0, expenditure: float = 0):
    logger.info("GET /api/v1/analytics/financial/utilization", allocated=allocated, expenditure=expenditure)
    logger.debug("Calling FinancialAnalytics.calculate_utilization_rate", allocated=allocated, expenditure=expenditure)
    try:
        result = FinancialAnalytics.calculate_utilization_rate(allocated, expenditure)
        logger.info("Utilization rate calculated successfully", result=str(result))
        return result
    except Exception as e:
        logger.error("Utilization calculation FAILED", exception=e, allocated=allocated, expenditure=expenditure)
        raise
