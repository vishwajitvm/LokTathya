# Phase 7A-2 Source Audit

This document records the database model and CRUD endpoints evidence for sources.

---

## 1. Physical Code Verification
- **Model File**: `backend/models/source.py`
- **Endpoints**: `/api/v1/sources` POST/GET/PATCH, `/api/v1/sources/{id}/endpoints` POST/GET, and `/api/v1/sources/endpoints/{ep_id}` PATCH.
- **Database Tables**: `src_source` and `src_endpoint`.

---

## 2. Test Execution
Verified by `test_acquisition_api.py::test_source_endpoints_modification_api` adding a source, adding an endpoint, and updating the endpoint status. All rows created are fully deleted in fixture teardown.
