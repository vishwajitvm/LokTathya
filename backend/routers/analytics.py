from fastapi import APIRouter
from analytics.financial import FinancialAnalytics
from analytics.metric_registry import registry

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])

@router.get("/metrics")
def get_metric_registry():
    return registry.metrics

@router.get("/financial/utilization")
def get_utilization(allocated: float = 0, expenditure: float = 0):
    return FinancialAnalytics.calculate_utilization_rate(allocated, expenditure)
