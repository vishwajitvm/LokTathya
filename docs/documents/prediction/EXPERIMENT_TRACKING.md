# Model Registry & Evaluation

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Technical Specification |
| Domain | PREDICTION |
| Subdomain | EXPERIMENT_TRACKING.MD |
| Status | ARCHITECTURAL |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Filename | EXPERIMENT_TRACKING.md |

---

## 1. Purpose
This document specifies the technical requirements, design constraints, operational details, and architectural integration rules of the `EXPERIMENT_TRACKING.md` component within the LokTathya platform. It acts as an authoritative reference for developers and system auditors.

## 2. Scope
This specification covers the implementation details of `EXPERIMENT_TRACKING.md` inside the `prediction` subsystem. It defines data structures, API contracts, processing pipelines, and validation requirements, ensuring consistency across both local containerized dev environments and production cloud architectures.

## 3. Problem Statement
The LokTathya civic intelligence system requires robust, isolated mechanisms to manage `EXPERIMENT_TRACKING.md` capabilities. Without structured, verifiable constraints, data processing and API integrations in this area can lead to inconsistencies, performance bottlenecks, and validation drift. This document addresses these concerns by establishing clean boundaries and validation rules.

## 4. Goals
The primary goals of this specification are:
* Ensure high reliability and validation parity across all environments.
* Provide clear guidelines for developers implementing features in this domain.
* Define strict error-handling and data recovery policies.
* Guarantee auditability of all data points and API transactions.

## 5. Non-Goals
This specification does not:
* Define external third-party API service implementations.
* Cover client-side user interface details (which are covered in frontend architecture specifications).
* Propose database schema changes (which are managed via migrations).

## 6. Architecture & Implementation
The architectural layout of `EXPERIMENT_TRACKING.md` is built around decoupled service boundaries. The system utilizes Celery tasks for background processing, PostgreSQL for relational storage, Redis for caching state, and FastAPI for routing requests. In the frontend, Next.js page components interact with backend routes via typed clients.

## 7. Data Model & Schema Details
All tables related to this domain are prefixed with `pre_` to ensure logical isolation. Schema columns enforce strict primary key limits, foreign key check constraints, and B-tree indexing on lookup fields. Geometries use SRID 4326 and are indexed using spatial GIST parameters.

## 8. API Contract & Communication
Communication between services is structured using JSON schemas. Routes validate payloads using Pydantic models. Every request is tagged with a `X-Request-ID` propagation header (TraceNest) to ensure transaction trace audit logs. Rate limits are set to 60 requests per minute per IP using Redis Token Buckets.

## 9. Source & Provenance Mapping
Every record processed in this domain must be linked back to a verified ID in the source registry (e.g. `SRC-IN-ECI-001`). This ensures complete data provenance. Direct calculations are annotated with audit markers to distinguish them from raw data.

## 10. Security & Privacy Controls
To protect user privacy and system integrity, several security controls are enforced:
* All input strings are sanitized against prompt injection and SQL injection patterns.
* Personal Identifiable Information (PII) like phone numbers and PAN numbers are redacted using regex filters before storage.
* Database connections use isolated network interfaces with no public ports exposed.

## 11. Error Handling & Failures
If an error occurs during parsing or validation:
* The database transaction is rolled back completely to prevent partial imports.
* The run state is set to `QUARANTINED` and written to the data quality logs.
* The background worker sends a traceback summary payload to the administration alerts channel.

## 12. Docker Runtime & Environment
All services run inside container networks using Docker Compose. The setup guarantees environment parity and prevents configuration drift. Developers exec commands using container boundaries (e.g. `docker compose exec backend pytest`).

## 13. TraceNest Logging & Observability
System logs are collected and structured in JSON format. Every run generates a unique run ID and logs started times, completed times, statuses, and row counts. Standard error outputs are captured in database records to assist developers in debugging.

## 14. Testing & Verification Plan
Validation is performed using automated unit and integration tests:
* Tests verify schema constraints and database relationships.
* Ingestion test cases run dummy files through the parser to test OCR fallback paths.
* Code must pass linter checks (black, flake8) and type audits (mypy).

## 15. Known Limitations & Future Work
Current limitations in this release include:
* Running heavy OCR jobs on large PDFs is memory-intensive and requires page splitting.
* Delimitation area comparisons are sensitive to geometry node sizes.
* Future releases will implement vector cache pre-fetching and parallel scraping pipelines.

## 16. Technical Details & Domain Constraints
Forecasting models are evaluated against baseline parameters. Training/testing sets use temporal splitting to prevent future data leakage. Active model metadata is registered in the database, allowing rollbacks if drift occurs.

## 17. Related Documents
* [FORECASTING_SCOPE.md](FORECASTING_SCOPE.md)
* [RESEARCH_WORKBENCH.md](../../features/10-research/RESEARCH_WORKBENCH.md)