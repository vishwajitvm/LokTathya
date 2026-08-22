import pytest
from core.celery_app import celery_app

def test_celery_task_routes():
    routes = celery_app.conf.task_routes
    assert routes is not None
    assert routes['ingestion.tasks.fetch_task'] == {'queue': 'fetch'}
    assert routes['ingestion.tasks.ocr_task'] == {'queue': 'ocr'}
    assert routes['ingestion.tasks.parse_gis'] == {'queue': 'gis'}
