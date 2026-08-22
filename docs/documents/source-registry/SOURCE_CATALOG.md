# Source Catalog Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Source Registry Catalog |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | National & State Data Sources |

---

## 1. Purpose
This document specifies the official data sources catalog, access methods, licensing parameters, and verification audits of the LokTathya platform.

---

## 2. Sourcing Registries

To maintain transparency, all data points in LokTathya are mapped to verified sources in this registry:

| Source ID | Name | Authority | Category | Official Domain | Verification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SRC-IN-ECI-001` | ECI Affidavits | Election Commission of India | ELECTIONS | `eci.gov.in` | VERIFIED |
| `SRC-IN-MOF-001` | Union Budgets | Ministry of Finance | FINANCE | `indiabudget.gov.in` | VERIFIED |
| `SRC-IN-SOI-001` | Boundary Files | Survey of India | GEOGRAPHY | `surveyofindia.gov.in` | VERIFIED |
| `SRC-ML-CEO-001` | Meghalaya CEO | CEO Meghalaya | ELECTIONS | `ceomeghalaya.nic.in` | VERIFIED |
| `SRC-MH-MUD-001` | Maharashtra UD | Urban Development Dept MH | FINANCE | `maharashtra.gov.in` | VERIFIED |

---

## 3. Data Licensing & Open Government License (OGL)

LokTathya aggregates datasets published under open data policies:
* **Primary License**: Government data is indexed under the **Government Open Data License - India (OGD)**, which permits non-commercial reuse, sharing, and compilation.
* **Attribution Requirement**: All exports, dashboards, and AI answers must display proper attribution citing the original department or authority.

---

## 4. Source Access Methods & Crawler Protocols

The system uses specific connectors based on the source data format:
* **API Access**: Used for platforms providing structured JSON or XML endpoints (e.g. data.gov.in portals).
* **HTML Scraping**: Extracted using clean parsing scripts, subject to rate limits.
* **Direct File Ingestion**: Scanned PDF nomination forms are downloaded, stored in MinIO, and parsed using OCR.
* **GIS Connectors**: Shapefiles and GeoJSON boundary files are imported using GDAL libraries inside the Celery worker container.

---

## 5. Verification & Ingestion Criteria

* **Source Authority**: Documents must originate from official `.gov.in` or `.nic.in` domains.
* **Cryptographic Signatures**: Sourced files are hashed (SHA-256) upon retrieval. Re-uploading files with matching hashes is blocked to prevent duplicate records.
* **Audit Trails**: Every database table includes a `source_id` column linking records back to this catalog.

---

## 6. Deprecation & Archiving Schedules

To maintain data integrity as source endpoints change:
* **Deprecation Log**: If a source endpoint changes (e.g. state assembly updates their document routing system), the source registry ID is marked as `DEPRECATED` and a redirection mapping is registered to route requests to the new endpoint.
* **Raw File Persistence**: Raw files ingested under deprecated source IDs are preserved in the MinIO archives to prevent broken links in historical dossiers.

---

## 7. State Archives Ingestion Schedule & Endpoint Mappings

To maintain regional data coverage:
* **Ingestion Triggers**: Celery tasks run daily to check for updates in CEO regional state websites.
* **State Directory Mappings**:
  * **Meghalaya**: `http://ceomeghalaya.nic.in/election-results/` (Form 20 PDF links).
  * **Maharashtra**: `http://maharashtra.gov.in/urban-development/` (Budget allocations sheets).

---

## 8. Source Compliance Auditing & Checkpoints

To ensure OGD compliance:
* **License Audits**: System administrators run quarterly checks to verify that indexed source files have not been subject to license updates or access policy changes.
* **Accessibility Checkpoints**: Auto-pings test the status of government portals daily, logging downtime in the source registry health dashboard.

---

## 9. Automated Error Isolation and Crawler Redirection

When a source portal becomes unresponsive:
* **Status Flags**: The source health status is set to `PORTAL_DOWNTIME`, prompting the scheduler to pause crawler tasks.
* **Failover URL Redirection**: If a secondary mirror registry exists (e.g. archive.org backups or verified NGO mirror repositories), crawler scripts fail over to the mirror endpoint to ensure ingestion continuity.

---

## 10. Source Registry Metadata Catalog Database Schema

To optimize search indexes across the registry:
* **Database Columns**: The `sources` table tracks `source_id`, `authority_name`, `license_type`, `crawling_frequency_days`, and `last_ingested_at`.
* **Index Configuration**: B-tree indexes are set on the `source_id` column to optimize queries from data quality tables.

---

## 11. Related Documents
* [INGESTION_PIPELINE.md](file:///c:/python/LokTathya/docs/documents/ingestion/INGESTION_PIPELINE.md)
* [VALIDATION_RECONCILIATION.md](file:///c:/python/LokTathya/docs/documents/data-quality/VALIDATION_RECONCILIATION.md)
