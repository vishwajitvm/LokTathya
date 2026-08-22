# Reports Generation Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Reporting Domain Specification |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | Constituency & Representative Dossier Exports |

---

## 1. Overview
This document specifies the reports compilation, snapshot versioning, template configuration, and asynchronous PDF generation services of the LokTathya platform. It details how data dossiers are built, archived, and exported for public consumption.

---

## 2. Problem Statement
Compiling comprehensive civic dossiers manually is time-consuming and prone to errors. When reporting on development projects, financial utilization, and legislative performance, the underlying data changes over time, making published reports hard to reproduce. We must automate dossier compilation, capture database snapshots, and export static PDF reports.

---

## 3. Goals
* **Automated Dossiers**: Compile multi-dimensional reports for constituencies or representatives.
* **Reproducible Snapshots**: Save database version snapshots to ensure report consistency.
* **Themed PDF Exports**: Export static, print-ready PDF files.

---

## 4. Non-Goals
* Providing real-time interactive dashboards within PDF files.

---

## 5. Target Users
* **Citizens**: Download comprehensive reports on their local representatives.
* **Researchers**: Export historical dossiers for local studies.
* **Journalists**: Print verified sheets to verify disclosures during debates.

---

## 6. User Stories
* As a citizen, I want to download a PDF report containing a representative's legislative record and active projects.
* As a researcher, I want to compare constituency dossiers across different delimitation cycles.

---

## 7. User Journey
1. **Navigate**: The user opens the `/reports` page.
2. **Configure**: The user selects a constituency or representative, selects a report template, and clicks "Generate Report".
3. **Download**: The backend compiles the report asynchronously and provides a download link for the PDF.

---

## 8. Functional Requirements
* **Dossier Compilation**: Aggregate data across geographic, representative, election, and project domains.
* **Snapshot Versioning**: Save database version snapshots with generated reports to ensure reproducibility.
* **PDF Exporter**: Render dynamic reports as static PDF documents using asynchronous tasks.

---

## 9. Data Requirements
* Compiled JSON datasets from database tables.
* Output storage bucket paths in MinIO for generated PDF files.

---

## 10. Backend Requirements
* **Celery Tasks**: Run report compilation tasks asynchronously to avoid blocking API servers.
* **PDF Compiler**: Convert JSON payloads into themed HTML and compile them to PDF format.

---

## 11. API Requirements
* `POST /api/v1/reports/compile`: Trigger an asynchronous report compilation task.
* `GET /api/v1/reports/{id}/download`: Get the download URL for the generated PDF.

---

## 12. Frontend Requirements
* Report creation forms with selectors for constituencies, representatives, and templates.
* Progress bars showing the status of active compilation tasks.

---

## 13. Responsive Requirements
* **Mobile**: Simplified selection forms. PDF files open directly in the browser's PDF viewer.
* **Desktop**: Side-by-side selectors and preview panels showing report templates.

---

## 14. Provenance Requirements
Every report must include a detailed source section listing the registry IDs of all documents used to compile the data.

---

## 15. Security Requirements
* **Rate Limiting**: PDF generation requests are rate-limited to prevent resource exhaustion attacks.
* **Access Control**: Public users can download completed reports, but triggering compilation tasks is restricted to registered users.

---

## 16. Error Handling
* **Compilation Failures**: If the PDF compiler fails, the task state is marked as `FAILED` and logs the error in the database.

---

## 17. Data Quality
The report generator verifies that all underlying data matches the latest verified database snapshots before starting compilation.

---

## 18. Performance
* Report compilation tasks are queued in Redis and processed by dedicated Celery workers to maintain API responsiveness.
* Generated PDF files are cached in MinIO to avoid redundant compilation runs.

---

## 19. Testing
Unit tests verify that report compilation tasks complete successfully and generate valid PDF files.

---

## 20. Acceptance Criteria
* PDF files render correctly and match the styling templates.
* Reports include complete source citations.
* Ingestion changes do not alter previously compiled static reports.

---

## 21. Limitations
* Large dossiers (e.g. state-level summaries) can take several minutes to compile, requiring page-load optimization.
* Complex PostGIS boundary coordinates are excluded from standard PDF reports to keep file sizes manageable.

---

## 22. Future Work
* Supporting custom scheduled reports (e.g. sending quarterly updates automatically).
* Integrating digital signatures to verify the authenticity of exported PDF files.

---

## 23. Related Documents
* [INTELLIGENCE_REPORTS.md](file:///c:/python/LokTathya/docs/documents/intelligence/INTELLIGENCE_REPORTS.md)
* [INGESTION_PIPELINE.md](file:///c:/python/LokTathya/docs/documents/ingestion/INGESTION_PIPELINE.md)
