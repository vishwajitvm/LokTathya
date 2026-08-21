from fastapi import APIRouter
from typing import Dict, Any
from ingestion.batch import IngestionBatchManager

router = APIRouter(prefix="/api/v1/ingestion", tags=["Ingestion Dashboard"])

@router.post("/batches")
def trigger_batch(source_ids: list[str], scope: str = "national"):
    return IngestionBatchManager.create_batch(source_ids, scope)

@router.get("/metrics")
def get_ingestion_metrics():
    # Mocking actual metrics collected from the deterministic framework
    return {
        "sources_scheduled": 5,
        "successful_fetches": 4,
        "failed_fetches": 1,
        "unchanged_content": 2,
        "new_content_versions": 2,
        "documents_parsed": 2,
        "parse_failures": 1,
        "canonical_records": 15000,
        "quarantined_records": 42
    }
