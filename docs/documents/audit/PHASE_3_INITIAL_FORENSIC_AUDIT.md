# Phase 3 Initial Forensic Audit Report

This report outlines the current architectural, database, ingestion, storage, API, and deployment state of the LokTathya codebase at the commencement of Phase 3 (National Source + Data Expansion Factory).

---

## 1. Repository Structure
The repository is split into two primary components:
- `backend/`: Standard Python FastAPI application containing endpoints, SQLAlchemy models, Alembic migrations, Celery task definitions, resilient HTTP clients, and custom parser factory components.
- `frontend/`: Next.js Web App using the App Router, containing interfaces for visualizing sources, documents, representative comparisons, and ingestion quality health reports.
- `docs/`: Holds design diagrams (`.mmd`), policy documents, and audit logs.

```
LokTathya/
├── backend/
│   ├── ai/
│   ├── alembic/
│   ├── analytics/
│   ├── connectors/
│   ├── core/
│   ├── data_quality/
│   ├── geography/
│   ├── ingestion/
│   ├── intelligence/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── storage/
│   └── tests/
├── frontend/
│   ├── app/
│   ├── components/
│   └── lib/
└── docs/
    ├── diagrams/
    └── documents/
```

---

## 2. Backend Architecture
The backend is built as a FastAPI service that communicates asynchronously with a PostgreSQL database, Redis broker, and MinIO raw object store. Core configurations and logging are managed through the TraceNest SDK, which hooks into FastAPI middleware to auto-inject request/correlation IDs across asynchronous worker execution boundaries.

---

## 3. Frontend Architecture
The frontend is built using Next.js 14 (React) with Tailwind CSS for layout styling. Page layouts map directly to specific features:
- `/sources`: Source listing and detail pages.
- `/representatives`: Profiles and metrics comparison.
- `/data-quality`: Tracks conflicts and anomalies across sources.
- `/civic-ai`: Chat panel integrating query planning and grounding.

---

## 4. Database Architecture
PostgreSQL with PostGIS extensions is the primary relational database. Data layouts are segregated into modules:
- `src_source`: Holds registered official data sources.
- `src_endpoint`: Endpoint configurations.
- `src_document` / `src_content_version`: Versioning engine.
- `src_observation`: Capture log separating raw from normalized values.
- `src_web_page` / `src_web_page_version` / `src_extracted_table`: Tracks web scrapers and unstructured extraction output.
- `prov_canonical_fact` / `prov_claim` / `prov_evidence`: Auditable provenance trail.

---

## 5. Docker Architecture
The system executes inside Docker using `docker-compose.yml` to define 7 long-running services:
1. `postgres`: Authoritative relational database.
2. `redis`: Broker for task queues and caching.
3. `minio`: Raw document object storage.
4. `backend`: Public-facing FastAPI HTTP app.
5. `worker`: Prefork concurrency Celery process.
6. `scheduler`: Cron-based heartbeat scheduler.
7. `frontend`: Next.js client application.

---

## 6. Ingestion Architecture
Ingestion begins when endpoints are fetched asynchronously by Celery task workers. Raw bytes are streamed straight to MinIO raw buckets and hashed. If the raw content hash differs from the latest stored ContentVersion, the format detector determines MIME types and dispatches to specific parsers. Parsed outputs are normalized and stored as observations.

---

## 7. Source Registry
The current registry defines a basic metadata layout. Currently, it has columns: `id`, `name`, `authority_name`, `authority_type`, `jurisdiction`, `category`, `official_domain`, `status`, `license`, `access_policy`.
This is insufficient for national-scale mapping which requires states like candidates, trust levels, state/district scopes, and next scheduled intervals.

---

## 8. Storage Implementation
The storage service is represented by `storage/minio_client.py`, which implements a `MinIOStorageService` wrapper around Boto3 client APIs. It handles uploads to `loktathya-raw` bucket, path generation, object checking, and streaming downloads securely.

---

## 9. Parser Implementation
A centralized `ParserFactory` manages content parsers for HTML, PDF, CSV, XLSX, and JSON documents. It extracts clean text, table dimensions, cell values, and outbound document references programmatically.

---

## 10. Versioning Implementation
Versioning is managed by generating unique UUIDs for ContentVersions linked to a primary Document identity. Content comparison relies on SHA-256 hashes. Same-content fetches only log events; changed contents trigger new ContentVersions.

---

## 11. Provenance Implementation
Provenance uses three core models: `CanonicalFact` (the authoritative fact), `Claim` (what a source says), and `Evidence` (links the Claim to the specific raw `Observation` table row). No fact can exist in the canonical layer without being traceable to a source document.

---

## 12. API Implementation
We have 14 FastAPI routers registered, including `sources`, `documents`, `web_pages`, and `ingestion`. API routes return structured JSON responses containing request IDs and pagination metadata.

---

## 13. Celery Implementation
Celery tasks are configured to run with Redis as the message broker. Task parameters are logged by TraceNest correlation keys, propagating correlation context from frontend requests to downstream processing loops.

---

## 14. Testing State
The test suite consists of 26 tests coveraging storage roundtrips, parser factory outputs, URL canonicalization, and SSRF prevention. All 26 tests pass cleanly.

---

## 15. Known Stubs, TODOs, and Mocks
- `routers/representatives.py` contains stub values for representative profile details.
- Conflict reconciliation relies on static consistent/conflict rules without advanced automated heuristics.
- Entity resolution uses high-confidence matching with stubs for human-in-the-loop review.
- GIS parser lacks shapefile validation checks.

---

## 16. Database Migration State
The migration head is aligned at `c184b591c559_add_observation_model`. All tables (observations, sources, versions, web pages) exist and conform to PK/FK guidelines.

---

## 17. Security & Scalability Weaknesses
- **Security**: SSRF checking is active for fetching but does not yet cover DNS rebinding protection window sizes.
- **Scalability**: Workers do not use separate dedicated Celery queues for heavy PDF OCR tasks, causing transient starvation of short HTML discovery jobs.
- **Access Safety**: Missing explicit policy files (e.g. `DATA_ACCESS_POLICY.md`) to categorize domain licensing boundaries.
