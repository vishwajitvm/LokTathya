# Representative Performance Tracker Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Legislative Domain Specification |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | National & State Legislators |

---

## 1. Overview
This document specifies the tracking parameters, legislative indicators, and performance evaluation metrics of public representatives (MPs/MLAs) in LokTathya. It outlines the criteria for measuring legislative activity and establishes guidelines to maintain political neutrality.

---

## 2. Problem Statement
Assessing the performance of public representatives is often subject to political bias and subjective interpretations. Third-party scoring systems create arbitrary "performance indices" that fail to reflect actual legislative contributions. We must define a factual, objective, and neutral system to compile representative activity metrics directly from official records.

---

## 3. Goals
* **Factual Compilation**: Focus on objective, verifiable metrics (attendance, questions asked, debates participated in).
* **Neutral Presentation**: Avoid subjective performance grades, ratings, or qualitative scores.
* **Traceable Activity**: Link every activity record (e.g. speech transcript, attendance log) back to its official source document.

---

## 4. Non-Goals
* Creating "best/worst legislator" lists, political grading systems, or qualitative scorecard indexes.

---

## 5. Target Users
* **Citizens & Voters**: Research local representatives' participation records and legislative activity.
* **Journalists**: Report on legislative activity and debate contributions using verified metrics.
* **Researchers**: Study legislative demographics, session participation trends, and debate focus areas.

---

## 6. User Stories
* As a citizen, I want to see the assembly session attendance rate of my local representative compared to the state average.
* As a journalist, I want to download speech transcripts and debate records for a representative to analyze their focus areas.

---

## 7. User Journey
1. **Navigate**: The user opens the `/representatives` directory page.
2. **Select Representative**: The user selects a representative profile.
3. **Audit**: The user opens the "Performance Tracker" tab to inspect session attendance records, questions raised during question hour, and debate contributions.

---

## 8. Functional Requirements
* **Session Attendance Rates**: Calculate and display attendance percentages:

$$\text{Attendance \%} = \left( \frac{\text{Days Present}}{\text{Total Session Days}} \right) \times 100$$

* **Question Hour Tracking**: Log and categorize questions raised by representatives (STARRED vs UNSTARRED).
* **Debate Speech Logs**: Link and display speech transcripts from assembly sessions.

---

## 9. Data Requirements
* Official session attendance registers published by Parliament and State Assemblies.
* Speech transcripts and question hour logs from official legislative bulletins.

---

## 10. Backend Requirements
* **Data Processing Tasks**: Celery workers run periodic tasks to parse session attendance and debate logs.
* **Transcript Storage**: Speech transcripts are stored in MinIO and indexed for quick retrieval.

---

## 11. API Requirements
* `GET /api/v1/representatives/{id}/performance`: Retrieve attendance, debate, and question hour metrics.
* `GET /api/v1/representatives/{id}/transcripts`: Retrieve speech transcripts.

---

## 12. Frontend Requirements
* Session attendance rate visualizers comparing individual figures to state/national averages.
* Speech transcript search interface within representative profiles.

---

## 13. Responsive Requirements
* **Mobile**: Attendance percentages shown on profile cards. Transcripts collapse into readable modules.
* **Desktop**: Full grid layouts with timeline visualizations of legislative contributions.

---

## 14. Provenance Requirements
Every activity record (attendance log, question raised, speech transcript) must link to its source file in the registry (e.g., `SRC-IN-LOKSABHA-001` Lok Sabha Bulletins).

---

## 15. Security Requirements
* **Data Integrity**: Legislative records are audited to prevent tampering.
* **Access Control**: Administrative updates to performance data require authorized credentials.

---

## 16. Error Handling
* **Missing Session Data**: If session attendance logs are unavailable for a specific legislature, the interface displays a `DATA_NOT_AVAILABLE` status for that period.

---

## 17. Data Quality
The ingestion task verifies that the total session days mapped to a representative do not exceed the actual length of the session.

---

## 18. Performance
Queries are indexed to load legislative performance metrics and transcripts in under 40ms.

---

## 19. Testing
Unit tests verify that attendance rate calculations are accurate.

---

## 20. Acceptance Criteria
* Performance metrics are compiled and presented without subjective grades or ratings.
* All figures link back to verified source files in the registry.
* Ingestion tasks validate session lengths before loading records.

---

## 21. Limitations
* Legislative attendance registers for some state assemblies are published with significant delays or are unavailable.
* Unofficial activities (constituency visits, local party meetings) are not tracked on the platform.

---

## 22. Future Work
* Integrating committee assignment attendance and participation metrics.
* Correlating legislative questions with constituency-specific development issues.

---

## 23. Related Documents
* [RELATIONAL_SCHEMA.md](file:///c:/python/LokTathya/docs/documents/data-model/RELATIONAL_SCHEMA.md)
* [DATA_GOVERNANCE.md](file:///c:/python/LokTathya/docs/features/99-governance/DATA_GOVERNANCE.md)
