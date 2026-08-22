# Phase 7A API Audit

This document records the endpoint inventory and schema verification.

---

## 1. Verified Route Inventory
- **POST /api/v1/ingestion/batches**: Creates database batch tracking record.
- **POST /api/v1/discovery/runs**: Triggers link crawler run.
- **POST /api/v1/discovery/candidates/{id}/approve**: Promotes Candidate status to ACTIVE.
- **PATCH /api/v1/sources/endpoints/{ep_id}**: Direct updates to endpoint properties.
