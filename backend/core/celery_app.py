from celery import Celery
import os

celery_app = Celery(
    "loktathya",
    broker=os.environ.get("REDIS_URL", "redis://redis:6379/0"),
    backend=os.environ.get("REDIS_URL", "redis://redis:6379/0")
)

celery_app.conf.task_routes = {
    'ingestion.tasks.source_discovery': {'queue': 'source_discovery'},
    'ingestion.tasks.fetch_task': {'queue': 'fetch'},
    'ingestion.tasks.parse_html': {'queue': 'html'},
    'ingestion.tasks.parse_pdf': {'queue': 'pdf'},
    'ingestion.tasks.ocr_task': {'queue': 'ocr'},
    'ingestion.tasks.parse_tabular': {'queue': 'tabular'},
    'ingestion.tasks.parse_gis': {'queue': 'gis'},
    'ingestion.tasks.normalize': {'queue': 'normalization'},
    'ingestion.tasks.resolve_entities': {'queue': 'entity_resolution'},
    'ingestion.tasks.reconcile': {'queue': 'reconciliation'},
}

@celery_app.task
def test_task():
    return "Infrastructure repaired"
