# Phase 7 Failure Handling & Quarantine

This document details isolation policies for ingestion failures.

---

## 1. Failure Isolation
- Ingestion tasks run in isolated Celery workers.
- Failures during single fetches are logged to `src_fetch_event` and quarantined in `src_quarantine` without stopping subsequent tasks in a batch run.
- Public APIs mask database trace logs to hide internal infrastructure details.
