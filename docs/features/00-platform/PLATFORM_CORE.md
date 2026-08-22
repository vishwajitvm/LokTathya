# Platform Core Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Technical Architecture & Platform Feature |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | Global Infrastructure |

---

## 1. Overview
This document specifies the core technical architecture, service orchestration, deployment topography, and containerized lifecycle management of the LokTathya platform. LokTathya is engineered as a decoupled, multi-container system running exclusively inside Docker-managed networks. It functions as a public infrastructure tool to aggregate, reconcile, audit, and expose Indian civic data and grounded AI insights to citizens, researchers, and administrators.

---

## 2. Problem Statement
Developing nationwide civic systems faces issues of data volatility, dependency version drift, configuration leakage, and host filesystem propagation delays. In multi-component stacks involving web applications, database servers, background workers, caching networks, and storage systems, local environment variations often cause synchronization errors. LokTathya solves this by implementing a strictly containerized, reproducible deployment stack.

---

## 3. Goals
* **Environment Replication**: Standardize execution environments using strict Docker configurations.
* **Component Decoupling**: Separate database queries, background tasks, static file hosting, and user interface rendering.
* **Observe and Trace**: Establish transaction tracing across container boundaries.
* **Ease of Contribution**: Simple bootstrap command to boot the entire stack and initialize relational tables.

---

## 4. Non-Goals
* Managing public hosting networks, DNS configuration, and production SSL load balancing.
* Designing proprietary, vendor-locked orchestration layers (e.g. cloud-specific serverless frameworks).

---

## 5. Target Users
* **Data Engineers**: Deploy and monitor data ingestion pipelines.
* **Software Developers**: Build user interfaces and backend routes.
* **System Auditors**: Verify execution logs and database transactions.

---

## 6. User Stories
* As a data engineer, I want to boot the entire stack with a single command so that I can focus on building parsing connectors instead of setting up local databases.
* As an administrator, I want transaction tracing across the frontend, API, and worker logs so that I can quickly debug ingestion or API errors.

---

## 7. User Journey
1. **Booting the Stack**: The developer clones the repository, copies the environment template, and runs `docker compose up -d --build`.
2. **Database Initialization**: The developer executes database migrations within the container boundary.
3. **Execution Verification**: The developer runs the test suite inside the backend container to confirm system integrity.

---

## 8. Functional Requirements
* **Container Orchestration**: Standardize Next.js, FastAPI, PostgreSQL, Redis, Celery, and MinIO components.
* **Volume Mapping**: Mount codebases for Next.js and FastAPI to sync changes instantly during development.
* **Hot-Reloading configuration**: Enforce filesystem watch configurations (e.g. `WATCHPACK_POLLING=true`) to resolve VM host-to-container mount delay issues on Windows.

---

## 9. Data Requirements
All components must access PostgreSQL, Redis, and MinIO via environment variables defined at container start. Local environment files (`.env`) are excluded from version control to prevent credential exposure.

---

## 10. Backend Requirements
* **FastAPI Gateway**: Exposes API endpoints and manages connection pools to database instances.
* **Celery Workers**: Consumes background tasks published to Redis.
* **Celery Scheduler**: Heartbeat daemon triggers cron tasks (e.g. synchronizing budget files).

---

## 11. API Requirements
* Expose API specs dynamically at `/docs` (OpenAPI format).
* Every response must include tracing headers:
  * `X-Request-ID`: TraceNest transaction ID.
  * `X-Process-Time`: Response processing time.

---

## 12. Frontend Requirements
* Single Page Application built on Next.js 14.
* Configure API proxy pass configurations mapping `/api/v1/*` routes to the FastAPI container gateway.

---

## 13. Responsive Requirements
Ensure the frontend matches responsive design paradigms:
* Mobile viewports (width < 768px): Stacked single-column layouts.
* Tablet viewports (768px to 1024px): Collapsible sidebars and grid structures.
* Desktop viewports (width > 1024px): Multi-pane side-by-side comparative views.

---

## 14. Provenance Requirements
Audit records must be automatically generated during migrations and data ingestion runs. Logs must capture task IDs, executing container hostnames, and database transactions.

---

## 15. Security Requirements
* **Network Isolation**: PostgreSQL, Redis, and MinIO must not expose their ports to the public host interface. Access is restricted to containers within the `loktathya_net` bridge network.
* **TraceNest logs**: Every HTTP request is assigned a unique transaction token (`X-Request-ID`). This ID is propagated as a comment in SQL queries to trace errors down to the database transactions.

---

## 16. Error Handling
* **API Exceptions**: Returns JSON payloads containing error codes and the corresponding request ID.
* **Connection Failures**: Implements auto-retry logic with exponential backoff on Celery database connection tasks.

---

## 17. Data Quality
Ensures that all tables are successfully created during Alembic migrations.

---

## 18. Performance
* Frontend compiles dynamically and utilizes Next.js Server-Side Rendering (SSR) for static pages to minimize loading times.
* Database uses indexes on geographical names and representative foreign keys to keep query latencies under 50ms.

---

## 19. Testing
Testing runs inside container boundaries using pytest:
```bash
docker compose exec backend pytest
```

---

## 20. Acceptance Criteria
* The stack builds and boots cleanly without errors.
* Rebuilding the container propagates code modifications instantly.
* The backend successfully runs migrations and passes all pytest test suites.

---

## 21. Limitations
* Filesystem watch polling (`WATCHPACK_POLLING=true`) increases CPU utilization on some host machines.
* PostGIS spatial indexing operations require pre-installing geos and proj libraries inside the database container.

---

## 22. Future Work
* Incorporating local Kubernetes configuration templates for production scaling.
* Integrating Prometheus metrics endpoints for container health monitoring.

---

## 23. Related Documents
* [RELATIONAL_SCHEMA.md](file:///c:/python/LokTathya/docs/documents/data-model/RELATIONAL_SCHEMA.md)
* [INGESTION_PIPELINE.md](file:///c:/python/LokTathya/docs/documents/ingestion/INGESTION_PIPELINE.md)
