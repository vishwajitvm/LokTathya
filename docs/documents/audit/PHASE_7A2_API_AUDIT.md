# Phase 7A-2 API Audit

This document records the OpenAPI routes inventory.

---

## 1. Verified Route Inventory
- **POST /api/v1/ingestion/batches**: Triggers ingestion batches.
- **POST /api/v1/discovery/runs**: Triggers link crawls.
- **POST /api/v1/discovery/candidates/{id}/approve**: Promotes Candidates to ACTIVE.
- **PATCH /api/v1/sources/endpoints/{ep_id}**: Modifies endpoint configuration.
