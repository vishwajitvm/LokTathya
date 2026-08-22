# LokTathya Data Access Policy

This document establishes the guidelines and protocols governing access to datasets, facts, and documents retrieved and processed by the LokTathya platform.

---

## 1. Objectives
The LokTathya platform operates as a national civic information infrastructure. The data access policy aims to:
- Preserve public transparency while adhering strictly to copyright, data privacy, and intellectual property limits.
- Ensure that authoritative data remains available without exposing raw personally identifiable information (PII) of private citizens.
- Prevent denial-of-service attempts on official sites during retrieval runs.

---

## 2. Classification of Data
LokTathya categorizes all ingested artifacts into specific security zones:

### A. Public Anonymous
- Content that is published openly by government entities with explicit permissive licenses (e.g. Creative Commons, Open Government License).
- Representative metrics, official budgets, and gazette notices.

### B. Public Attribution Required
- Datasets requiring explicit references and copyright text inclusions to be served in raw form.
- Embeddings generated from press releases where the original source URI must accompany downstream grounding responses.

### C. Restricted/Confidential
- Auditable provenance records containing metadata of internal staging runs.
- Temporary ingestion cache data representing parsed tables under active reconciliation.

---

## 3. Storage and Object Access Boundaries
- Raw PDF, CSV, and XML downloads are placed in MinIO buckets with read/write access limited to internal celery workers.
- The public API may only serve structured extracted JSON records containing provenance links.
- Direct downloads of raw binary blocks are served using pre-signed temporary URLs with short validity windows (e.g. 15 minutes).

---

## 4. Legal Compliance Guidelines
- Compliance with the Information Technology Act and relevant regional data protection bills.
- If a government department issues a retraction, tombstone, or correction, the platform maintains the historical hash state but marks the record status as `SUPERSEDED` or `WITHDRAWN` according to versioning rules.
- Data deletion requests (Right to be Forgotten) regarding non-representative public profiles are handled through human-in-the-loop review.
