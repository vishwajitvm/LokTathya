# Phase 7A-2 Discovery Audit

This document records discovery, sitemaps index, RSS, and candidates review endpoints evidence.

---

## 1. Physical Code Verification
- **File**: `backend/ingestion/discovery.py`
- **Method**: `discover_sitemap` and `discover_rss`.
- **API Paths**: `/api/v1/discovery/runs` GET/POST, `/api/v1/discovery/candidates` GET, and `/api/v1/discovery/candidates/{id}/approve` POST.

---

## 2. Test Execution
Verified by `test_acquisition_api.py::test_discovery_runs_and_candidates_api` running a mock candidate URL, listing discovery runs, and approving the candidate to transition status to `ACTIVE`.
