# Phase 7A-3 Runtime Evidence Report

This document records the physical execution trace of active containers, migrations, and APIs.

---

## 1. Clean-Room Container State
```bash
docker compose ps
```
### Result
All 7 services are running and healthy:
- `loktathya_backend` (Up)
- `loktathya_frontend` (Up)
- `loktathya_minio` (healthy)
- `loktathya_postgres` (healthy)
- `loktathya_redis` (healthy)
- `loktathya_scheduler` (Up)
- `loktathya_worker` (Up)

---

## 2. Celery Worker Registered Task Mappings
```bash
docker exec loktathya_backend celery -A core.celery_app inspect registered
```
### Result
```text
->  celery@a1dc01412b4d: OK
    * core.celery_app.test_task
    * ingestion.tasks.fetch_task
    * ingestion.tasks.normalize
    * ingestion.tasks.ocr_task
    * ingestion.tasks.parse_gis
    * ingestion.tasks.parse_html
    * ingestion.tasks.parse_pdf
    * ingestion.tasks.parse_tabular
    * ingestion.tasks.poll_scheduler
    * ingestion.tasks.reconcile
    * ingestion.tasks.resolve_entities
    * ingestion.tasks.source_discovery
```

---

## 3. Database Migration Revision Check
```bash
docker exec -e PYTHONPATH=/app loktathya_backend alembic current
```
### Result
```text
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
d9634a538d9c (head)
```
