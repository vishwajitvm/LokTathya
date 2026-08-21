from fastapi import APIRouter
from typing import Dict, Any
from source_registry.coverage import CoverageEngine
from source_registry.health import SourceHealthTracker

router = APIRouter(prefix="/api/v1/coverage", tags=["Source Coverage"])

@router.get("/{jurisdiction_id}")
def get_jurisdiction_coverage(jurisdiction_id: str, category: str = None):
    # Mocking single category coverage
    return CoverageEngine.calculate_coverage(jurisdiction_id, category or "elections")

@router.get("/health/{source_id}")
def get_source_health(source_id: str):
    return SourceHealthTracker.ping_source(source_id, "https://mock.gov.in/api")
