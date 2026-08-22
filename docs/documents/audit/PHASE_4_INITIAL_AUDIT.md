# Phase 4 Initial Forensic Audit Report

This report outlines the baseline assessment of the LokTathya codebase for the Phase 4 development of the National Data Acquisition & Processing Factory.

---

## 1. Codebase Scan for Stubs & Hardcoded Logic
A search across all repository paths has identified interfaces and implementation definitions that require expansion for Phase 4 production capabilities.

### A. NotImplementedError Traces
- `backend/ingestion/interfaces.py`: `BaseConnector` defines `discover`, `fetch`, `parse`, and `validate` methods returning `NotImplementedError`.
- `backend/ingestion/pdf_processor.py`: `OCRProvider.extract_text` raises `NotImplementedError`. `TesseractProvider` is a stub returning simulated text values.

### B. Mocks & Stubs
- `backend/ingestion/pdf_processor.py`: Contains a mock chunker (`PDFChunker.chunk`) returning simulated array structures.
- `backend/routers/discovery.py` & `backend/routers/quarantine.py`: New endpoints created in Phase 3 return hardcoded JSON payloads for discovery candidates, runs, and quarantine list operations.

---

## 2. Docker Baseline Assessment
The `docker-compose.yml` configures 7 central services:
- `postgres` (using custom `database/Dockerfile`)
- `redis:7-alpine`
- `minio/minio`
- `backend` (FastAPI application listening on port 8000 mapped to 8001 on the host)
- `worker` (Celery worker executing `celery -A core.celery_app worker`)
- `scheduler` (Celery beat executing `celery -A core.celery_app beat`)
- `frontend` (Next.js Node application running on port 3000)

All container healthchecks use built-in CLI tests (`pg_isready` for PostgreSQL, `redis-cli ping` for Redis, and standard HTTP curls for MinIO).

---

## 3. Database Schema Baseline
The active migration history is verified under `backend/alembic/versions/`. The head migration is `f1c2c1d84e03_p3_registry_endpoint_expansion.py`.
The schema contains PostGIS extensions (`postgis`) and `pgvector` enabled inside the database init script, with tables defined for:
- `src_source`
- `src_endpoint`
- `src_dataset`
- `src_ingestion_run`
- `src_fetch_event`
- `src_document`
- `src_content_version`
- `src_web_page`
- `src_web_page_version`
- `src_observation`
- `src_claim`
- `src_evidence`
- `src_canonical_fact`
