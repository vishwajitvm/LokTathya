# Phase 5 Initial Forensic Audit

This report records the repository audit for Phase 5 of LokTathya.

---

## 1. Audit of Models and Entities

### A. Observation
- `src_observation` exists inside `backend/models/observation.py`.
- Columns: `id`, `source_id`, `document_id`, `content_version_id`, `web_page_id`, `web_page_version_id`, `entity_type`, `field_name`, `raw_value`, `normalized_value`, `extraction_location`, `observed_at`, `status`.

### B. Entity Resolution
- `sys_entity_resolution` exists inside `backend/models/resolution.py`.
- Columns: `id`, `source_id`, `raw_value`, `target_table`, `candidate_id`, `matching_method`, `confidence`, `status`, `reviewer`, `resolved_at`.

### C. Provenance & Canonical Fact
- `prov_claim`, `prov_canonical_fact`, `prov_evidence` exist inside `backend/models/provenance.py`.
- Models support tracing canonical facts to underlying source claims and evidence.

---

## 2. Inconsistencies and Production Gaps
- **Reconciliation Engine**: Currently parses and compares dates inside `backend/data_quality/reconciliation.py` but is not fully integrated with the observation pipeline to produce `CanonicalFact` entries automatically.
- **Entity Resolution Engine**: String fallback method in `backend/ingestion/entity_resolution.py` is simple. We need to implement robust exact matching, geographic/temporal contextual matching, and review queue updates.
- **Normalization pipeline**: Type normalization functions (handling Indian numbering system like crore/lakh, Rupees, etc.) are partially mock/missing in the ingestion parser pipeline. We need a unified Normalization service.
