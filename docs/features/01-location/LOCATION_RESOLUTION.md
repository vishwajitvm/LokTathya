# Location Resolution Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Geographical Domain Specification |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | National / Constituency Level |

---

## 1. Overview
This document specifies the location resolution system, geographic hierarchies, boundary versioning cycles, and spatial query integrations of the LokTathya platform. Geographic data in LokTathya maps civic boundaries over multiple delimitation cycles, linking coordinates with representatives, elections, and budgets.

---

## 2. Problem Statement
Civic boundaries in India are not static. Parliamentary and Assembly constituencies shift their geographical borders during Delimitation cycles to account for population changes. Mapping historic election results or project funds to dynamic boundaries causes data discrepancies. We must build a PostGIS-enabled database that supports boundary versioning.

---

## 3. Goals
* **Geographical Continuity**: Maintain records of historical boundary boundaries across delimitation cycles.
* **Point-in-Constituency Resolution**: Resolve GPS coordinate inputs to their matching Assembly and Parliamentary constituencies.
* **Spatial Relationship Modeling**: Identify neighboring districts and constituencies.

---

## 4. Non-Goals
* Providing real-time navigation routes or mapping non-civic features (e.g. roads, commercial points of interest).

---

## 5. Target Users
* **Data Engineers**: Import boundary shapefiles (SHP) or GeoJSON files.
* **Voters & Citizens**: Locate their representatives by providing GPS coordinates or searching for their address.
* **Researchers**: Study changes in election outcomes and voter distributions across delimitation cycles.

---

## 6. User Stories
* As a citizen, I want to allow the browser to access my GPS location so that I can immediately identify my local MP and MLA.
* As a data engineer, I want to map imported GeoJSON datasets to specific delimitation cycles so that historical boundaries are preserved.

---

## 7. User Journey
1. **Search Initiation**: The user navigates to the `/geography` page.
2. **Location Entry**: The user types a constituency name or clicks "Use Current Location" to provide GPS coordinates.
3. **Information Retrieval**: The backend maps the input to a constituency record and retrieves active projects, representative profiles, and election history.

---

## 8. Functional Requirements
* **Hierarchical Resolution**: Track States ➡️ Districts ➡️ constituencies ➡️ Wards.
* **Delimitation Cycle Tracking**: Every boundary coordinate must link to a specific delimitation cycle (e.g., 2002 cycle).
* **Multi-polygon Support**: Support complex boundary geometries with enclave exceptions.

---

## 9. Data Requirements
* Shapefiles or GeoJSON boundaries sourced from the **Survey of India** or the **Election Commission of India (ECI)**.
* Geometry coordinate reference system: **SRID 4326** (WGS 84).

---

## 10. Backend Requirements
* **PostGIS Extension**: Enabled inside the PostgreSQL database.
* **Spatial Queries**: Use functions like `ST_Contains` for coordinates and `ST_Touches` for adjacent boundaries.

---

## 11. API Requirements
* `GET /api/v1/geographies/`: Query list of states, districts, and constituencies.
* `GET /api/v1/geographies/locate/`: Resolves latitude and longitude inputs to a constituency record.

---

## 12. Frontend Requirements
* Interactive SVG or Leaflet map display on the `/geography` page.
* Accessible list fallback index for browsers without WebGL capabilities.

---

## 13. Responsive Requirements
* **Mobile**: Single-column layout. The map collapses into a drawer, prioritizing list results.
* **Desktop**: Split screen showing the map on the left and constituency details on the right.

---

## 14. Provenance Requirements
Every geographic record must link to its source file in the registry (e.g. `SRC-IN-SOI-001` Survey of India Shapefiles).

---

## 15. Security Requirements
User coordinates provided for location resolution are processed in-memory and are not persisted in database logs to protect user privacy.

---

## 16. Error Handling
* **Out-of-Bounds Location**: If coordinates fall outside India's borders, the API returns a `LOCATION_OUT_OF_BOUNDS` error.
* **Ambiguous Search**: If a constituency name exists in multiple states (e.g., "Aurangabad"), the API returns both choices for disambiguation.

---

## 17. Data Quality
Boundary geometries are validated using `ST_IsValid` during ingestion to prevent self-intersecting loops and ensure clean data.

---

## 18. Performance
* Spatial columns use **GIST** index structures to keep boundary lookup latency under 30ms.
* Large boundary geometries are simplified using `ST_SimplifyPreserveTopology` to optimize frontend render times.

---

## 19. Testing
Automated tests verify point-in-polygon queries using coordinate test cases:
* Shillong coordinates `(91.88, 25.57)` must resolve to the Shillong constituency.

---

## 20. Acceptance Criteria
* GPS coordinates successfully resolve to the correct constituency.
* Changing the delimitation cycle filter updates the boundary map display.
* Invalid boundary geometries are rejected during ingestion.

---

## 21. Limitations
* Historical boundary data prior to the 1973 delimitation cycle is often incomplete or exists only as text descriptions.
* Administrative district boundaries do not always align with election constituency borders.

---

## 22. Future Work
* Integrating demographic data layers (e.g. census statistics) onto the constituency map.
* Supporting temporal boundary animation to visualize constituency shifts over time.

---

## 23. Related Documents
* [RELATIONAL_SCHEMA.md](file:///c:/python/LokTathya/docs/documents/data-model/RELATIONAL_SCHEMA.md)
* [HISTORICAL_GEOGRAPHY.md](file:///c:/python/LokTathya/docs/documents/geography/historical/HISTORICAL_GEOGRAPHY.md)
