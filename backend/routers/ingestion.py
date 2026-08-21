from fastapi import APIRouter, BackgroundTasks
import uuid

router = APIRouter(prefix="/api/v1/ingestion", tags=["Ingestion"])

@router.post("/{source_id}/ingest")
def trigger_ingestion(source_id: uuid.UUID, background_tasks: BackgroundTasks):
    from ingestion.tasks import run_ingestion_pipeline
    # In a real app we'd dispatch to Celery. For FastAPI dummy we could use background_tasks or just return a dummy task_id.
    task_id = str(uuid.uuid4())
    run_ingestion_pipeline.delay(str(source_id), "http://dummy", "data_gov")
    return {"ingestion_run_id": task_id, "status": "QUEUED"}
