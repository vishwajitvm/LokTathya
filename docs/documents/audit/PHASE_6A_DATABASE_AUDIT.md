# Phase 6A Database Audit

This document records the forensic validation of database schemas and migrations.

---

## 1. Verified Tables and Constraints

- **geo_entity / geo_relationship**: Contains multipolygon geography and parent-child delimitation trees.
- **rep_person / rep_term / rep_party**: Maps representatives, parties, and legislative sessions.
- **elec_election / elec_result**: Election metrics and rank attributes.
- **proj_project / proj_work / proj_tender / proj_contract**: Project implementation schemas.
- **fin_budget / fin_allocation / fin_release / fin_expenditure**: Financial tracing tables.
- **prov_canonical_fact / prov_claim / prov_evidence**: Tracing canonical records back to original fetched documents.
