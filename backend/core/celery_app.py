from celery import Celery
import os

celery_app = Celery(
    "loktathya",
    broker=os.environ.get("REDIS_URL", "redis://redis:6379/0"),
    backend=os.environ.get("REDIS_URL", "redis://redis:6379/0")
)

@celery_app.task
def test_task():
    return "Infrastructure repaired"
