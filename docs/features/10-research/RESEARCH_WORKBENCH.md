# Research Workbench Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Research Interface Specification |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | Custom Civic Research & Analytics |

---

## 1. Overview
This document specifies the research workflows, correlation builders, custom query engines, and dataset exploration interfaces of the Research Workbench in LokTathya. The Research Workbench enables researchers, journalists, and academics to perform detailed civic analysis across multiple datasets.

---

## 2. Problem Statement
Academic research on Indian civic systems is often hindered by fragmented data sources and the lack of tools to correlate representative activity, election histories, and development spending. Exporting data for analysis typically requires writing custom scraper scripts. We must provide a structured, safe query builder to filter, correlate, and export civic datasets.

---

## 3. Goals
* **Correlation Metrics**: Enable users to correlate datasets (e.g. comparing constituency turnout rates with victory margins).
* **Comparative Visuals**: Side-by-side charts and correlation matrices.
* **Safe Exports**: Support exporting filtered datasets in standard formats (CSV, JSON).

---

## 4. Non-Goals
* Running probabilistic modeling or predictive forecasting within the interface (prediction is documented separately).

---

## 5. Target Users
* **Academics & Researchers**: Study long-term trends in legislative demographics and spending.
* **Journalists**: Build data-driven investigative stories.
* **NGOs & Policy Advocates**: Audit project spending and legislative performance.

---

## 6. User Stories
* As a researcher, I want to plot a scatter chart comparing representative attendance rates with project completion rates in their constituencies.
* As a journalist, I want to filter and export the declared assets of all representatives who switched political parties in the last decade.

---

## 7. User Journey
1. **Explore**: The user opens the `/intelligence` page.
2. **Select Parameters**: The user selects datasets, filters by year or geography, and chooses correlation indicators.
3. **Analyze**: The UI renders correlation tables, scatter plots, and trends.
4. **Export**: The user clicks "Export Dataset" to download the data as a CSV file.

---

## 8. Functional Requirements
* **Correlation Analysis**: Identify correlations between representative attendance, questions raised, and project completions.
* **Custom Query Builder**: Let users filter datasets by state, year, party, and delimitation cycle.
* **Data Exporter**: Support exporting datasets in CSV and JSON formats.

---

## 9. Data Requirements
* Indexes of representatives, constituencies, projects, and elections from core database tables.
* Source metadata and storage paths from the `sources` registry table.

---

## 10. Backend Requirements
* **Query Compiler**: Translates structured filter requests into safe PostgreSQL queries.
* **SQL Injection Defenses**: The backend validates parameters to prevent arbitrary SQL execution.

---

## 11. API Requirements
* `GET /api/v1/intelligence/correlate`: Retrieve correlation values for selected indicators.
* `GET /api/v1/intelligence/export`: Download filtered datasets.

---

## 12. Frontend Requirements
* Interactive charts (scatter, line, bar) showing correlation trends.
* Grid displays showing side-by-side comparisons of representatives or constituencies.

---

## 13. Responsive Requirements
* **Mobile**: Simplified tables. Detailed charts are replaced by descriptive summary blocks.
* **Desktop**: Full workspace layout with side-by-side query builders, interactive charts, and export options.

---

## 14. Provenance Requirements
Every exported dataset must include a citation index mapping the records back to their original source document registry IDs.

---

## 15. Security Requirements
* **Rate Limiting**: Export requests are rate-limited to protect server resources.
* **SQL Isolation**: Users cannot execute raw SQL; queries are compiled using safe parameters.

---

## 16. Error Handling
* **Empty Results**: If no data matches the selected filters, the interface displays an empty state with suggestions to adjust query parameters.
* **Query Timeouts**: If a custom query takes too long, the system aborts the request and returns a timeout error.

---

## 17. Data Quality
The Research Workbench alerts users if they attempt to compare datasets with low confidence scores or mismatched delimitation cycles.

---

## 18. Performance
* Complex analytical queries are cached in Redis to keep response times under 50ms.
* Export files are compiled asynchronously using background Celery tasks.

---

## 19. Testing
Unit tests verify that the query compiler generates valid SQL and does not execute unauthorized statements.

---

## 20. Acceptance Criteria
* Correlation calculations are mathematically accurate.
* Exported files contain complete source citations.
* The query compiler blocks arbitrary SQL execution.

---

## 21. Limitations
* Inconsistencies in historical data limits comparison ranges for elections prior to 2004.
* PostGIS geometry columns are excluded from standard CSV exports due to file size constraints.

---

## 22. Future Work
* Integrating advanced statistical modules (e.g. regression analysis) directly into the UI.
* Supporting collaborative dashboards so researchers can share custom query views.

---

## 23. Related Documents
* [FORECASTING_SCOPE.md](file:///c:/python/LokTathya/docs/documents/prediction/FORECASTING_SCOPE.md)
* [DETERMINISTIC_METRICS.md](file:///c:/python/LokTathya/docs/documents/analytics/DETERMINISTIC_METRICS.md)
