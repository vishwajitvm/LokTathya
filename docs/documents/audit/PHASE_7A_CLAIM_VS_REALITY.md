# Phase 7A Claim vs Reality Audit

This document records the forensic comparison between the claimed capabilities of Phase 7 and the actual state verified in the repository.

---

## 1. Verification Registry

| Feature Claim | Actual Code | Actual Runtime | Test | Evidence | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **URL Canonicalization** | `URLCanonicalizer` inside `backend/core/url_canonical.py` | Normalizes host/ports/slash/parameters | `test_url_canonicalizer.py` | 1 passed in 0.51s | PASS |
| **robots.txt Compliance** | `AccessPolicyManager` inside `backend/core/access_policy.py` | Respects disallow policies of target hosts | `test_access_policy.py` | 1 passed in 0.54s | PASS |
| **Sitemap Indexes** | Recursive parser inside `ControlledDiscoveryEngine.discover_sitemap` | Fetches nested sitemap paths | `test_discovery.py` | Part of discovery test | PASS |
| **Ingestion Batches API** | `/api/v1/ingestion/batches` inside `backend/routers/ingestion.py` | Queries `src_ingestion_batch` table | `test_acquisition_api.py` | 4 passed in 3.35s | PASS |
| **Discovery Runs API** | `/api/v1/discovery/runs` inside `backend/routers/discovery.py` | Queries `src_ingestion_run` table | `test_acquisition_api.py` | 4 passed in 3.35s | PASS |
| **Quarantine / Coverage** | `/api/v1/coverage` and `/api/v1/quarantine` | Database query checks | `test_acquisition_api.py` | 4 passed in 3.35s | PASS |
