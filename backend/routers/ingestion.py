from fastapi import APIRouter
from typing import Dict, Any
from tracenest import logger
from ingestion.batch import IngestionBatchManager

router = APIRouter(prefix="/api/v1/ingestion", tags=["Ingestion Dashboard"])

@router.post("/batches")
def trigger_batch(source_ids: list[str], scope: str = "national"):
    logger.info("POST /api/v1/ingestion/batches – Triggering new ingestion batch", source_count=len(source_ids), scope=scope)
    logger.debug("Batch source IDs", source_ids=str(source_ids), scope=scope)
    logger.debug("Delegating to IngestionBatchManager.create_batch", source_count=len(source_ids))
    try:
        result = IngestionBatchManager.create_batch(source_ids, scope)
        logger.info("Ingestion batch triggered successfully", batch_result=str(result)[:200])
        return result
    except Exception as e:
        logger.error("Ingestion batch trigger FAILED", source_ids=str(source_ids), scope=scope, error=str(e))
        raise

@router.get("/metrics")
def get_ingestion_metrics():
    logger.info("GET /api/v1/ingestion/metrics – Fetching ingestion pipeline metrics")
    logger.debug("Assembling ingestion metrics snapshot")
    metrics = {
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
    logger.info("Ingestion metrics returned", total_sources=metrics["sources_scheduled"], success_rate=f"{metrics['successful_fetches']}/{metrics['sources_scheduled']}")
    return metrics
