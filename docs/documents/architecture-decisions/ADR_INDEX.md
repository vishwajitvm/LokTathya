# Architecture Decision Records Index

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Architecture Decisions Index |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | Global Architecture Decisions |

---

## 1. Purpose
This document indexes the Architectural Decision Records (ADRs) of the LokTathya platform, detailing historical design decisions, rationales, and consequences.

---

## 2. ADR Index

### A. ADR-0001: Strict Dockerization of Development Environment
* **Status**: ACCEPTED
* **Date**: 2026-08-20
* **Context**: LokTathya runs a decoupled stack with Next.js, FastAPI, PostgreSQL, Redis, Celery, and MinIO. Setting up these dependencies on developer host machines causes version mismatches.
* **Problem**: How do we ensure execution environment parity across development, testing, and production environments?
* **Options Considered**:
  * *Option 1*: Local package manager configurations (npm, pip, homebrew, chocolatey).
  * *Option 2*: Docker Compose based multi-container environment.
* **Decision**: Adopt a strictly containerized Docker Compose environment. All development commands, migrations, and test suites must run inside container boundaries.
* **Rationale**: Docker guarantees environment consistency and prevents configuration drift.
* **Consequences**: Developers do not need to install dependencies locally, but must run all operations inside container shells (e.g. `docker compose exec`).

---

### B. ADR-0002: Grounded LLM Tool Routing (CivicTools)
* **Status**: ACCEPTED
* **Date**: 2026-08-21
* **Context**: The Civic AI assistant requires access to database records to answer natural-language queries.
* **Problem**: How do we grant the LLM access to database tables while preventing SQL injection vulnerabilities and hallucinated statistics?
* **Options Considered**:
  * *Option 1*: LLM compiles and executes raw SQL queries directly on the database.
  * *Option 2*: LLM uses predefined, typed tools (`CivicTools`) that return structured context.
* **Decision**: Restrict the LLM to pre-defined `CivicTools` endpoints. The LLM cannot write or execute raw SQL.
* **Rationale**: Pre-defined tools prevent SQL injection attacks and ensure the LLM only accesses validated database records.
* **Consequences**: Adding new query capabilities requires defining a new tool endpoint in the backend codebase.

---

### C. ADR-0003: PostGIS & pgvector DB Integrations
* **Status**: ACCEPTED
* **Date**: 2026-08-21
* **Context**: LokTathya requires geographical constituency boundary queries and vector similarity queries.
* **Problem**: How do we support boundary overlaps and vector similarity queries without adding multiple database instances?
* **Options Considered**:
  * *Option 1*: Separate spatial (e.g. Esri) and vector (e.g. Pinecone) database platforms.
  * *Option 2*: Single PostgreSQL database with PostGIS and pgvector extensions.
* **Decision**: Single PostgreSQL database running PostGIS and pgvector.
* **Rationale**: Reduces operational complexity and keeps all data transactions within a single relational store.
* **Consequences**: High-dimension HNSW indexes require configuring dedicated memory pools inside the database container.

---

### D. ADR-0004: Asynchronous Ingestion Workers using Celery and Redis
* **Status**: ACCEPTED
* **Date**: 2026-08-21
* **Context**: Ingesting scanned PDFs, executing OCR, and reconciling candidate data takes time and can block the main API response thread.
* **Problem**: How do we handle heavy ingestion runs without degrading API performance?
* **Options Considered**:
  * *Option 1*: Execute ingestion inline in the API request thread.
  * *Option 2*: Delegate ingestion to background workers using Celery and Redis.
* **Decision**: Adopt Celery background workers with Redis as a message broker.
* **Rationale**: Asynchronous processing prevents API gateway timeouts and allows scaling worker containers independently.
* **Consequences**: Requires managing worker container lifecycles and logging tasks in a status table.

---

### E. ADR-0005: Standardized PDF Document Archive with MinIO
* **Status**: ACCEPTED
* **Date**: 2026-08-22
* **Context**: LokTathya indexes candidate affidavits, CAG audit sheets, and budget files that need to be made available to the public.
* **Problem**: Where do we store and serve raw documents to ensure provenance check audits?
* **Options Considered**:
  * *Option 1*: Save files directly on the API container's host filesystem.
  * *Option 2*: Use an S3-compatible object storage server (MinIO).
* **Decision**: Use MinIO as an S3-compatible local object storage server.
* **Rationale**: S3 compatibility makes it easy to transition to cloud storage (e.g. AWS S3) in production.
* **Consequences**: Requires managing bucket access policies and handling file upload keys.

---

## 3. Related Documents
* [PLATFORM_CORE.md](file:///c:/python/LokTathya/docs/features/00-platform/PLATFORM_CORE.md)
* [CIVIC_AI_ARCHITECTURE.md](file:///c:/python/LokTathya/docs/documents/ai/CIVIC_AI_ARCHITECTURE.md)
