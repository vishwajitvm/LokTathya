# Phase 6 Initial API Audit

This report records the initial audit of LokTathya API endpoints.

---

## 1. Audit Matrix of Existing APIs

| Endpoint | Router Exists | Implementation | DB Query | Real PostgreSQL | Provenance | Pagination |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **GET /api/v1/geographies** | Yes | Stub (returns empty) | No | No | No | Yes (parameters only) |
| **GET /api/v1/representatives** | Yes | Stub (returns empty) | No | No | No | No |
| **GET /api/v1/elections** | Yes | Stub (returns empty) | No | No | No | Yes (parameters only) |
| **GET /api/v1/projects** | No | Missing | No | No | No | No |
| **GET /api/v1/finance/budgets** | No | Missing | No | No | No | No |
| **GET /api/v1/documents** | Yes | Missing `GET /` and diff/provenance | Yes (partial) | Yes (partial) | No | No |
| **GET /api/v1/web-pages** | Yes | Missing `GET /` and tables | Yes (partial) | Yes (partial) | No | No |
| **GET /api/v1/sources** | Yes | Real (mostly complete) | Yes | Yes | No | Yes |

---

## 2. Gaps and Actions
- We need to write proper database queries matching the schemas for Geography, Representative, Election, Project, Finance, and Document.
- Location coordinate lookup using PostGIS is missing. We need to implement `/api/v1/location/resolve` and `/api/v1/location/{id}/profile`.
- We need to ensure every domain service uses a common response contract containing `data_quality` and `provenance`.
