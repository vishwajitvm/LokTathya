# Relational Schema Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Database Schema Specification |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | Relational Database Schema |

---

## 1. Purpose
This document specifies the database schemas, entity relationships, primary/foreign keys, spatial configurations (PostGIS), and vector definitions (pgvector) of the LokTathya platform. It matches the SQLAlchemy models implemented in the codebase.

---

## 2. Entity-Relationship Topology

```
+------------------+         +-----------------------+         +------------------+
|   Geographies    |-------->|    Representatives    |<--------|  Constituencies  |
|  (States/Dist)   |         |     (MPs / MLAs)      |         |  (Boundaries)    |
+------------------+         +-----------------------+         +------------------+
         |                               |                              |
         v                               v                              v
+------------------+         +-----------------------+         +------------------+
|     Sources      |         |       Elections       |         |   Data Quality   |
| (Provenance Reg) |         |   (Vote Counts/BOs)   |         | (Conflicts Logs) |
+------------------+         +-----------------------+         +------------------+
```

---

## 3. Database Table Definitions

### A. Table: `states`
Stores regional state configurations:
* `state_code` (VARCHAR(5), Primary Key): Unique code classification (e.g. `IN-ML`).
* `state_name` (VARCHAR(100), Unique, Not Null): Name of the state.
* `type` (VARCHAR(50), Not Null): `STATE` vs `UNION_TERRITORY`.

### B. Table: `constituencies`
Stores electoral boundary polygons:
* `id` (UUID, Primary Key): Unique identifier.
* `state_code` (VARCHAR(5), Foreign Key mapping to `states.state_code`): State link.
* `constituency_name` (VARCHAR(150), Not Null): Name of the constituency.
* `type` (VARCHAR(50), Not Null): `PARLIAMENTARY` vs `ASSEMBLY`.
* `boundary` (GEOMETRY(MULTIPOLYGON, 4326), Not Null): Polygon coordinates.
* `delimitation_cycle_id` (UUID, Foreign Key mapping to `delimitation_cycles.id`): Cycle link.

### C. Table: `representatives`
Stores representative bio data:
* `id` (UUID, Primary Key): Unique identifier.
* `full_name` (VARCHAR(200), Not Null): Name of the representative.
* `gender` (VARCHAR(20), Not Null).
* `date_of_birth` (DATE, Nullable).
* `party_id` (UUID, Foreign Key mapping to `political_parties.id`): Party link.
* `biography_vector` (VECTOR(1536), Nullable): Vector embedding for semantic search.

### D. Table: `representative_terms`
Tracks legislative careers:
* `id` (UUID, Primary Key): Unique identifier.
* `representative_id` (UUID, Foreign Key mapping to `representatives.id`): Representative link.
* `house` (VARCHAR(50), Not Null): `LOK_SABHA`, `RAJYA_SABHA`, or `VIDHAN_SABHA`.
* `constituency_id` (UUID, Foreign Key mapping to `constituencies.id`): Constituency link.
* `start_date` (DATE, Not Null).
* `end_date` (DATE, Nullable).

---

## 4. Indexing & Optimization Strategy

1. **Spatial Indexing**: A **GIST** index is configured on the `constituencies.boundary` column to optimize point-in-polygon queries.
2. **Vector Indexing**: An **HNSW** index is configured on the `representatives.biography_vector` column to optimize semantic search retrieval times.
3. **Primary/Foreign Keys**: Indexes are automatically generated on all foreign key columns to optimize join operations.

---

## 5. Related Documents
* [LOCATION_RESOLUTION.md](file:///c:/python/LokTathya/docs/features/01-location/LOCATION_RESOLUTION.md)
* [REPRESENTATIVES_DIRECTORY.md](file:///c:/python/LokTathya/docs/features/02-representatives/REPRESENTATIVES_DIRECTORY.md)
