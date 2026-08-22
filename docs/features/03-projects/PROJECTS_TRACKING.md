# Projects Tracking Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Infrastructure Tracking Domain Specification |
| Status | PARTIALLY_IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | Constituency Development Projects |

---

## 1. Overview
This document specifies the public works project tracking system, contractor registers, tender records, and budget utilization monitoring configurations (MPLADS/MLACDF) in the LokTathya platform. It bridges administrative project data with geographic constituencies and public funding allocations.

---

## 2. Problem Statement
Monitoring local development projects suffers from fragmented progress reports, unclear contractor attributions, and a lack of geographic mapping. Budgets for constituency development funds (MPLADS) are often declared as lump sums, making it difficult to trace funds to individual projects. We must associate projects with specific geographical bounds and financial transactions.

---

## 3. Goals
* **Spatial Attribution**: Map public works projects to constituency boundaries.
* **Audit Trail**: Track the progress of projects from the planned stage through completion.
* **Funding Accountability**: Monitor fund disbursals and expenditures against project estimates.

---

## 4. Non-Goals
* Managing real-time worker logs, daily site updates, or acting as a project management tool for contractors.

---

## 5. Target Users
* **Citizens**: Monitor local public works projects in their neighborhoods.
* **Journalists**: Investigate delayed projects or contractor performance trends.
* **Auditors**: Verify that spent funds match the physical progress of projects.

---

## 6. User Stories
* As a citizen, I want to see all ongoing road construction projects in my assembly constituency.
* As an auditor, I want to see if a project marked as complete has been verified by an independent municipal audit.

---

## 7. User Journey
1. **Explore**: The user opens the `/projects` page.
2. **Filter**: The user filters by constituency, project status (ongoing, completed), or contractor.
3. **Audit Inspection**: The user selects a project to view its funding allocations, tender details, and audit status.

---

## 8. Functional Requirements
* **Lifecycle Tracking**: Track projects through `PLANNED`, `ONGOING`, `COMPLETED`, `STALLED`, and `CANCELLED` statuses.
* **Geographic Mapping**: Store GPS coordinates for projects using PostGIS point features.
* **Funding Linkages**: Map project expenditures to MPLADS or municipal budget accounts.

---

## 9. Data Requirements
* Tender publications and project progress logs from state e-procurement portals.
* Disbursal and expenditure sheets from the Ministry of Statistics and Programme Implementation (MoSPI).

---

## 10. Backend Requirements
* **Spatial Relationship Processing**: Link projects to constituencies using PostGIS `ST_Contains` lookups on project coordinates.
* **Reconciling Data**: Parse CSV and XML feeds from e-procurement portals and resolve duplicate projects.

---

## 11. API Requirements
* `GET /api/v1/projects/`: Get projects list with status filters.
* `GET /api/v1/projects/{id}/budget`: Retrieve allocated vs spent values.

---

## 12. Frontend Requirements
* Display projects on the constituency map page using status-colored coordinate markers.
* Progress bars showing budget utilization percentages.

---

## 13. Responsive Requirements
* **Mobile**: Show a list of local projects sorted by distance from the user.
* **Desktop**: Map view with a details panel that slides open when a project is selected.

---

## 14. Provenance Requirements
Every project must link to its e-procurement tender ID or government sanction order number.

---

## 15. Security Requirements
Access to administrative interfaces (such as updating project status or flagging overruns) is restricted to verified auditors.

---

## 16. Error Handling
* **Missing Coordinates**: Projects with missing GPS coordinates default to the centroid of their target constituency.

---

## 17. Data Quality
The system flags anomalies, such as when the amount spent exceeds the allocated budget, for review.

---

## 18. Performance
Spatial queries are indexed to load local projects within 40ms.

---

## 19. Testing
Unit tests verify that projects are linked to the correct constituency based on coordinate inputs.

---

## 20. Acceptance Criteria
* Projects map correctly to constituency boundaries.
* Budget utilization calculations are accurate.
* Anomaly flags are triggered for budget overruns.

---

## 21. Limitations
* Contractor registers are often incomplete on state portals, limiting attribution tracking.
* GPS coordinates provided in public tenders can be inaccurate or point to general administrative offices.

---

## 22. Future Work
* Integrating citizen-reported photo updates to verify project status.
* Correlating contractor performance histories with project delays.

---

## 23. Related Documents
* [RELATIONAL_SCHEMA.md](file:///c:/python/LokTathya/docs/documents/data-model/RELATIONAL_SCHEMA.md)
* [PUBLIC_FINANCE.md](file:///c:/python/LokTathya/docs/features/04-finance/PUBLIC_FINANCE.md)
