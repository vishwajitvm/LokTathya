# Phase 4 Stub and NotImplemented Forensic Audit

This document records the audit of placeholders, NotImplementedError instances, stubs, and mocks within the LokTathya codebase.

---

## 1. Mocks and Stubs Audit List

### A. Legitimate Test Mocks
- `backend/tests/test_connector.py` / `test_discovery.py` / `test_security_hardening.py`: Using `unittest.mock.patch` to isolate HTTP client requests from external networks. This ensures fast, reliable, offline-capable unit execution inside Docker sandbox networks.

### B. Production Gaps (Resolved)
- `backend/data_quality/reconciliation.py`: `evaluate_observations` previously assumed observation B was newer without parsing dates. This has been updated to systematically parse and compare ISO date strings.

### C. Standard fallbacks / Deterministic matchers
- `backend/ingestion/entity_resolution.py`: Implements a fast, deterministic string matcher fallback using exact lookup mappings. This is fully database-backed and avoids fragile heuristic frameworks.
- `backend/geography/historical.py`: Static boundaries for delimitation events. Temporal boundary forecasting is deferred from Phase 4 production (advanced analytics).

### D. Dead Code
- `backend/ingestion/fetch_task.py`: Contains a legacy simulation module. Since the Phase 4 engine utilizes `UniversalConnector` with MinIO storage client logic in `tasks.py`, `fetch_task.py` is dead/ignored code.
