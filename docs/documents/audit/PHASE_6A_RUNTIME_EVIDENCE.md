# Phase 6A Runtime Evidence

This document records the runtime trace of active containers, logs, and database queries.

---

## 1. Verified Services

- **FastAPI backend**: Reloader active and openapi endpoint responding on `http://localhost:8001/api/v1/openapi.json`.
- **Celery Worker**: Binding 11 active task queues (`celery`, `fetch`, `pdf`, etc.).
- **PostgreSQL / PostGIS**: Healthy connection pool responding to queries under 50ms.
