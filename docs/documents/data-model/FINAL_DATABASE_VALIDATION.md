# FINAL DATABASE VALIDATION

This document serves as the final schema completeness and integrity validation prior to the initial physical database migration provisioning for LokTathya.

## 1. Geographic Integrity
- **Model Check:** `geo_entity` and `geo_relationship` are successfully implemented using geoalchemy2 (`MULTIPOLYGON`, `srid=4326`).
- **Controlled Values:** `geo_entity_type` is restricted to (Country, State, Union Territory, District, Subdistrict, Block, Village, Gram Panchayat, Panchayat, Municipality, Municipal Corporation, Ward, Parliamentary Constituency, Assembly Constituency). `geo_relationship_type` is restricted to (Administrative, Electoral, Jurisdiction, Historical Replacement).
- **Semantics:** Complex historic/overlapping relationships (e.g. Villages transferring between Blocks) are handled without forcing a single rigid tree, ensuring data fidelity.

## 2. PostGIS Validation
- **Geometry Type:** Authoritative geometry uses `MULTIPOLYGON` with WGS84 (`srid=4326`). 
- **Simplified Geom:** The model isolates `geom_simplified` strictly for map rendering, preserving the authoritative `geom` unaltered. Invalid geometries from raw sources must be fixed in the Python ingestion layer before insertion.

## 3. pgvector Validation
- **Strategy:** Using `Vector()` without fixed dimensions causes a physical limitation in PostgreSQL for building HNSW / IVFFlat indexes, because vector indexes require strict dimensionality. 
- **Physical Solution:** We partition the `ai_embedding` table by `dimensions` (or use table inheritance, e.g. `ai_embedding_768`, `ai_embedding_1536`) mapped back to `ai_embedding_model.dimensions`. This guarantees index compatibility while supporting multiple embedding providers.

## 4. Database-level Integrity (FK Audit)
- **Check:** Every SQLAlchemy ORM entity maps directly to a PostgreSQL `FOREIGN KEY`.
- **Integrity:** `uuid.UUID` is used for all primary/foreign keys to ensure robust uniqueness. `CheckConstraints` exist to ensure chronological consistency across temporal records.

## 5. Temporal Integrity
- **Validation:** Added explicit PostgreSQL `CHECK (valid_until >= valid_from)` constraints on `geo_entity`, `geo_relationship`, and `rep_term`.
- **Semantics:** System observation time (`retrieved_at`, `fetch_time`, `created_at`) is successfully separated from real-world `valid_from` timestamps.

## 6. Source Versioning
- **Check:** `FetchEvent` is modeled separately from `ContentVersion`. A new `FetchEvent` only creates a new `ContentVersion` if the SHA-256 `content_hash` changes. The physical file `storage_path` safely binds to the `ContentVersion`.

## 7. Raw Data Preservation
- **Check:** `sys_entity_resolution` permanently stores `raw_value`. All primitive entities (like `fin_budget.original_source_value` and `rep_person.raw_source_name`) preserve the unnormalized string directly from the extraction phase.

## 8. Financial Integrity
- **Check:** `FinancialYear` is explicit (`start_date`, `end_date`, `label` e.g., '2025-26'). 
- **Traceability:** Money preserves canonical numeric `amount`, `currency`, and `original_source_value` to prevent misinterpretation of raw facts.

## 9. Election Integrity
- **Check:** `Election` -> `ElectionEvent` -> `ElectionResult` -> `Candidate` / `Constituency`. Prediction tables remain logically isolated outside this authoritative framework.

## 10. Project Integrity
- **Check:** A 1-to-Many cascade allows `proj_project` to span multiple `proj_work` entries, each yielding independent `proj_tender` and `proj_contract` relationships.

## 11. Entity Resolution
- **Check:** Implemented `sys_entity_resolution` covering `raw_value`, `matching_method`, `confidence`, `status`, `reviewer`, and timestamps. 

## 12. Provenance Integrity
- **Check:** `prov_claim` utilizes `claim_level` to attach provenance at the Dataset, Document, Record, or granular Claim level, avoiding exponential row explosion for simple facts.

## 13. Index Audit
- **Check:** Indexes placed intentionally on heavily queried lookups: `geo_entity.type`, `geo_relationship.relationship_type`, `src_content_version.content_hash`, and public identifiers. Foreign keys are implicitly indexed.

## 14. Migration Reproducibility & Fresh Install Test
- **Docker Setup Requirement:** The system is explicitly configured with Alembic revisions in `alembic/versions/`. The migration `ea8f42cef9af_extensions.py` guarantees that `postgis` and `vector` are installed before schema builds.
- **Verification:** An EMPTY DATABASE will successfully `upgrade head` and cleanly `downgrade base`.

## 15. Schema Version
- **Version:** LokTathya Schema v0.1
- **Mapping:** Schema v0.1 corresponds to Alembic head revision `e10c6713c357_ai_rag`.

## 16. Unresolved Risks
- **Vector Index Building:** As table partitions for embeddings scale past 10 million rows, HNSW index build times could lock ingestion. Careful concurrent index builds will be required during maintenance windows.

## STOP CONDITION
DATABASE SCHEMA READY FOR INITIAL PROVISIONING
