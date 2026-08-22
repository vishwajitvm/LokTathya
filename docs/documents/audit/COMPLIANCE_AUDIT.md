# Compliance Audit Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Audit & Compliance Specification |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | Quality Assurance & Security Compliance |

---

## 1. Purpose
This document specifies the compliance audit protocols, validation checks, and security audit checklists of the LokTathya platform. It defines the parameters for testing and deployment verification.

---

## 2. Platform Audit Checklist

Every deployment must pass the following compliance audits:

### A. Docker Infrastructure Audit
* **Check ID**: `AUD-DKR-001`
* **Expected**: All service containers (Next.js, FastAPI, PostgreSQL, Redis, Celery, MinIO) boot and communicate over the internal `loktathya_net` bridge network.
* **Observed**: Next.js (port 3000) and FastAPI docs (port 8001) are accessible. Database, cache, and object storage instances are isolated.
* **Status**: PASS
* **Notes**: Verified via `docker compose ps` checks.

---

### B. Security & Isolation Audit
* **Check ID**: `AUD-SEC-001`
* **Expected**: Database instances must not bind or publish their ports to external host interfaces.
* **Observed**: PostgreSQL, Redis, and MinIO ports are unmapped in `docker-compose.yml` to prevent public connections.
* **Status**: PASS
* **Notes**: Verified by running port scans on the host machine interface.

---

### C. Database Migration Audit
* **Check ID**: `AUD-MIG-001`
* **Expected**: Run database migrations to initialize the 33 relational tables and spatial/vector extensions.
* **Observed**: Alembic upgrade tasks complete successfully without SQL errors.
* **Status**: PASS
* **Notes**: Verified via `docker compose exec backend alembic current`.

---

### D. Data Quality & PII Redaction Audit
* **Check ID**: `AUD-DQ-001`
* **Expected**: Nomination affidavits and budget files ingested into the database must be scrubbed of PAN numbers and phone contacts.
* **Observed**: PAN card strings match regex filters and are replaced with redaction placeholders. Phone numbers are redacted.
* **Status**: PASS
* **Notes**: Verified by checking representative asset profiles in the database.

---

### E. TraceNest Integration Audit
* **Check ID**: `AUD-TRC-001`
* **Expected**: Every API request and response is assigned a transaction token (`X-Request-ID`), which is propagated to standard logs.
* **Observed**: Logging middleware extracts and prints the request ID for all incoming traffic.
* **Status**: PASS
* **Notes**: Verified by checking backend container stdout logs.

---

### F. API Documentation & Rate Limiting Audit
* **Check ID**: `AUD-API-001`
* **Expected**: API endpoints expose OpenAPI metadata correctly at `/api/v1/openapi.json` and enforce active rate limits of 60 requests per minute.
* **Observed**: FastAPI successfully outputs the schema definitions, and rate-limiting modules block requests that exceed limits.
* **Status**: PASS
* **Notes**: Verified using postman endpoints and curl tests.

---

### G. AI Grounding & Validation Audit
* **Check ID**: `AUD-AI-001`
* **Expected**: The Civic AI assistant only generates answers using retrieved context and does not output ungrounded claims.
* **Observed**: The prompt evaluation engine halts responses when context is missing, outputting `DATA_NOT_AVAILABLE`.
* **Status**: PASS
* **Notes**: Verified using prompt injection test cases.

---

### H. Geographical Geometry Audit
* **Check ID**: `AUD-GEO-001`
* **Expected**: Boundary coordinates are saved as valid multipolygon coordinate systems.
* **Observed**: Invalid geometries (e.g. self-intersecting loops) are rejected during the ingestion parse step.
* **Status**: PASS
* **Notes**: Verified via `ST_IsValid` database checks.

---

## 3. Related Documents
* [PLATFORM_CORE.md](file:///c:/python/LokTathya/docs/features/00-platform/PLATFORM_CORE.md)
* [VALIDATION_RECONCILIATION.md](file:///c:/python/LokTathya/docs/documents/data-quality/VALIDATION_RECONCILIATION.md)
