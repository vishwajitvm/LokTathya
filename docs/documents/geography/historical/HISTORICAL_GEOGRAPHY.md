# Historical Geography Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Geographical Domain Historical Specification |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | Spatial Boundary Versioning |

---

## 1. Purpose
This document specifies the spatial database models, PostGIS boundary calculations, and delimitation cycles tracking rules for boundary versioning in the LokTathya platform.

---

## 2. Background
Constituency boundaries are redrawn periodically by Delimitation Commissions. Comparing election results or development projects across different cycles requires checking for shifts in boundaries. We use PostGIS geometry fields to model and verify boundary modifications over time.

---

## 3. Delimitation Cycles Registry

The database stores boundary polygons grouped by delimitation cycles (1952, 1963, 1973, 2002):
* `constituencies.boundary` geometry columns are indexed using spatial **GIST** structures.
* The system evaluates spatial overlaps between boundaries in different cycles to determine comparability.

---

## 4. PostGIS Overlap Calculations

The database uses PostGIS to calculate boundary overlap percentages:

$$\text{Overlap \%} = \left( \frac{\text{Area}(\text{Boundary A} \cap \text{Boundary B})}{\text{Area}(\text{Boundary A})} \right) \times 100$$

### SQL Implementation Example:
```sql
SELECT 
  a.constituency_name AS name_a,
  b.constituency_name AS name_b,
  (ST_Area(ST_Intersection(a.boundary, b.boundary)) / ST_Area(a.boundary)) * 100 AS overlap_percentage
FROM constituencies a, constituencies b
WHERE a.delimitation_cycle_id = :cycle_a_id
  AND b.delimitation_cycle_id = :cycle_b_id
  AND ST_Intersects(a.boundary, b.boundary);
```

---

## 5. Temporal Geometry & Boundary Overlay Logic

To handle changes in boundary shapes over time, the system uses spatial geometry filters:
* **`ST_Union`**: Used to group constituency fragments when a single boundary is split into multiple parts between cycles.
* **`ST_Difference`**: Identifies areas added or removed from a constituency boundary.
* **Non-Comparable States**: If a state splits or undergoes major boundary changes (e.g. Bihar/Jharkhand in 2000), direct historic comparisons across boundaries are blocked, and the system requires a manual disclaimer.

---

## 6. Spatial Resolution & Projection Systems

* **SRID 4326**: All geometries are stored using the WGS 84 geographic coordinate system (latitude/longitude) to allow maps to render in web clients.
* **Area Calculation Projection (SRID 32643)**: To calculate area overlaps accurately, geometries are temporarily projected to UTM Zone 43N (SRID 32643) during calculations. This prevents distortions caused by spherical coordinate systems:

```sql
ST_Area(ST_Transform(boundary, 32643))
```

---

## 7. Simplification & Topological Validation

* **Topology Preservation**: Geometries are simplified using `ST_SimplifyPreserveTopology` with a tolerance of `0.001` degrees. This reduces polygon node counts, optimizing database queries and map load times without causing gap overlap errors:

```sql
ST_SimplifyPreserveTopology(boundary, 0.001)
```

* **Validity Testing**: The ingestion task runs `ST_IsValidReason` on all boundary shapefiles, sending self-intersecting or open polygon records to the quarantine database.

---

## 8. Boundary Revision and Enclave Resolution

* **Enclave Mapping**: Some historical constituencies contain land enclaves (exclaves) separated by other regions. PostGIS `ST_NumGeometries` is used to count and index disjoint polygons under a single multi-polygon record.
* **Revision History Tracking**: Boundary modifications are saved with a timeline, ensuring that active project attributions link to the correct shape file in use at the project's start date.

---

## 9. Boundary Scale Thresholds

To prevent map loading lag in low-bandwidth areas:
* **Node Limit**: Simplified multi-polygons are restricted to a maximum of 5,000 coordinate nodes per constituency.
* **Simplification Fallback**: If a geometry simplification fails to maintain topology, the task defaults to a slightly lower precision threshold, logging a warning flag in the build output.

---

## 10. Data Compression and Vector Tile Servicing

To reduce map load times on mobile clients:
* **Mapbox Vector Tiles (MVT)**: PostGIS queries use `ST_AsMVT` to serve boundary coordinates as compressed vector tiles directly to the web client, bypassing JSON formats.
* **Cache Headers**: MVT tiles are cached at the CDN level with standard Cache-Control headers to reduce load on the database container.

---

## 11. Related Documents
* [LOCATION_RESOLUTION.md](file:///c:/python/LokTathya/docs/features/01-location/LOCATION_RESOLUTION.md)
* [HISTORICAL_ELECTIONS.md](file:///c:/python/LokTathya/docs/documents/elections/historical/HISTORICAL_ELECTIONS.md)
