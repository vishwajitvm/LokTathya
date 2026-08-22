# Election Analytics Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Election Domain Specification |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | National & State Elections |

---

## 1. Overview
This document specifies the election database structures, voter turnout analysis, swing calculations, and polling-booth level analytics of the LokTathya platform. It details how results are ingested, validated, and normalized across different election cycles.

---

## 2. Problem Statement
Analyzing election data over time is complicated by boundary shifts during delimitation cycles and variations in candidate name spellings across different election files. Comparing vote share swings between consecutive elections requires mapping constituencies across delimitation cycles. We must build a database schema that models these relationships and handles candidate identity resolution.

---

## 3. Goals
* **Temporal Comparability**: Compare election results across boundary shifts.
* **Fuzzy Identity Matching**: Resolve variations in candidate name spellings to single representative profiles.
* **Granular Analytics**: Track election results down to the individual polling booth level.

---

## 4. Non-Goals
* Running predictive election models or publishing opinion poll forecasts.

---

## 5. Target Users
* **Voters**: Research historical election results and candidate records in their constituencies.
* **Journalists**: Track changes in vote shares, swings, and victory margins.
* **Researchers**: Study micro-level voter behavior using booth-level results.

---

## 6. User Stories
* As a journalist, I want to see the vote share swing for a political party in a constituency between the 2019 and 2024 general elections.
* As a researcher, I want to download polling-booth level vote tallies for a constituency to analyze spatial voting patterns.

---

## 7. User Journey
1. **Search**: The user navigates to the `/elections` dashboard.
2. **Select Election**: The user selects a Lok Sabha or Vidhan Sabha election year.
3. **Audit**: The user reviews the overall results map, filters by constituency, and drills down to booth-level data.

---

## 8. Functional Requirements
* **Turnout Rate Calculations**: Calculate voter turnout rates by constituency:

$$\text{Turnout \%} = \left( \frac{\text{Total Votes Polled}}{\text{Total Registered Voters}} \right) \times 100$$

* **Vote Share Swing Calculations**: Track support shifts for political parties:

$$\text{Swing} = \text{Vote Share \% (Current Election)} - \text{Vote Share \% (Previous Election)}$$

* **Constituency Match Mapping**: Map constituencies across boundary delimitation cycles.

---

## 9. Data Requirements
* Detailed election results publications (Form 20/21E) from the Election Commission of India (ECI).
* State-level Chief Electoral Officer (CEO) bulletins.

---

## 10. Backend Requirements
* **Fuzzy Matching Module**: Resolve spelling variations of candidate names using fuzzy matching logic (e.g. Levinshtein distance).
* **Ingestion Pipelines**: Parse ECI results feeds and verify totals.

---

## 11. API Requirements
* `GET /api/v1/elections/`: Get lists of general elections.
* `GET /api/v1/elections/results/`: Get constituency-level result breakdowns.

---

## 12. Frontend Requirements
* Interactive state-level results maps.
* Visualization charts showing swing trends.

---

## 13. Responsive Requirements
* **Mobile**: Show a list of candidates sorted by vote count.
* **Desktop**: Map view with a details panel showing candidate list, swings, and margins side-by-side.

---

## 14. Provenance Requirements
Every election result must link to its source file in the registry (e.g., `SRC-IN-ECI-001` ECI results portals).

---

## 15. Security Requirements
* **Access Control**: Administrative changes to election records require authorized credentials.
* **Data Integrity**: Election database transactions are audited to prevent tampering.

---

## 16. Error Handling
* **Vote Count Mismatches**: If the sum of votes from polling booths does not match the constituency's declared vote total, the system flags the record as `VOTE_COUNT_MISMATCH` for review.

---

## 17. Data Quality
The ingestion task verifies that candidate vote counts sum up to the total valid votes polled.

---

## 18. Performance
Queries are indexed by election year, candidate ID, and constituency ID to keep load times under 40ms.

---

## 19. Testing
Unit tests verify that candidate name variations (e.g. "Conrad Sangma" vs "Conrad K. Sangma") are successfully matched or flagged.

---

## 20. Acceptance Criteria
* Turnout and swing calculations are accurate.
* Polling booth results match the constituency totals.
* Name variations are resolved to single profiles.

---

## 21. Limitations
* Name resolution fuzzy matching logic can generate false positives for candidates with common names (e.g., "John Smith"), requiring manual review.
* Booth-level data for older elections (prior to 2004) is often unavailable.

---

## 22. Future Work
* Integrating candidate assets and criminal records disclosures onto the election results pages.
* Correlating voter turnout rates with demographic census data layers.

---

## 23. Related Documents
* [RELATIONAL_SCHEMA.md](file:///c:/python/LokTathya/docs/documents/data-model/RELATIONAL_SCHEMA.md)
* [HISTORICAL_ELECTIONS.md](file:///c:/python/LokTathya/docs/documents/elections/historical/HISTORICAL_ELECTIONS.md)
