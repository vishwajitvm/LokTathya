# Representatives Directory Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Legislative Domain Specification |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | National & State Legislatures |

---

## 1. Overview
This document specifies the representatives registry, multi-term tracking, political party changes, and financial/criminal disclosure tracking systems of the LokTathya platform. It acts as the technical reference for managing legislative portfolios of MPs and MLAs.

---

## 2. Problem Statement
Legally mandated disclosures by political candidates in India are filed in scanned PDF formats containing handwritten pages or tables. Tracking a representative's career across multiple terms and parties is difficult due to name variations (e.g. spelling changes) and shifts in constituency names. We must normalize these records into a clean, queryable database.

---

## 3. Goals
* **legislative career History**: Track representatives' movements across constituencies, houses, and political parties.
* **Audit Transparency**: Link financial and criminal disclosures to verified nomination affidavits.
* **Neutral Data Presentation**: Present candidate data objectively without qualitative rankings.

---

## 4. Non-Goals
* Assigning qualitative performance grades, political opinions, or scoring representatives' character.

---

## 5. Target Users
* **Voters**: Research local candidates' asset changes and criminal disclosures before voting.
* **Journalists**: Investigate changes in representative asset portfolios over time.
* **Researchers**: Analyze party-switching trends and legislative demographics.

---

## 6. User Stories
* As a citizen, I want to compare the declared assets of a representative across three consecutive terms.
* As an investigator, I want to see a representative's active court cases and the corresponding IPC sections charged.

---

## 7. User Journey
1. **Search**: The user enters a representative's name (e.g., "Conrad Sangma") in the `/representatives` page.
2. **Profile Load**: The profile loads showing their current photo, party affiliation, and legislative history.
3. **Disclosure Inspection**: The user opens the "Disclosures" tab to audit asset tables, liability schedules, and court cases.

---

## 8. Functional Requirements
* **Multi-Term Tracking**: Connect multiple legislative terms (MLA, MP) to a single representative profile.
* **Party Affiliation Timeline**: Track changes in party affiliation, including splits and mergers.
* **Disclosures Parsing**: Capture Movable/Immovable Assets, Liabilities, and Criminal Cases.

---

## 9. Data Requirements
* Scanned nomination affidavits (Form 26) published by the Election Commission of India.
* Official legislative directories from Parliament and State Assemblies.

---

## 10. Backend Requirements
* **OCR Processing Tasks**: Celery workers run OCR text extraction on scanned PDFs.
* **Reconciliation Module**: Merges spelling variations of candidate names using fuzzy matching logic (e.g. Levinshtein distance).

---

## 11. API Requirements
* `GET /api/v1/representatives/`: Search and filter representatives.
* `GET /api/v1/representatives/{id}/disclosures`: Get asset, liability, and court records.

---

## 12. Frontend Requirements
* Comparative profile card views with timeline visualizers for legislative terms.
* Link indicators pointing back to the original affidavit PDF.

---

## 13. Responsive Requirements
* **Mobile**: Single card view. Details expand into collapsible accordions.
* **Desktop**: Grid layout comparing multiple profiles side-by-side.

---

## 14. Provenance Requirements
Every financial figure or criminal charge must contain a `source_id` linking back to its original document in the registry.

---

## 15. Security Requirements
* **PII Redaction**: Private phone numbers, tax IDs (PAN), and bank account numbers are redacted during ingestion.
* **Access Control**: Administrative changes to representative profiles require authorized credentials.

---

## 16. Error Handling
* **Duplicate Profile Identified**: fuzzy matching flags potential duplicate records for manual admin review rather than merging them automatically.

---

## 17. Data Quality
Declared totals are mathematically validated against their individual line item sums to identify errors in original files.

---

## 18. Performance
Queries are indexed by candidate names and constituency IDs to ensure profile load times remain under 40ms.

---

## 19. Testing
Tests verify that fuzzy name matches (e.g. "Conrad Sangma" vs "Conrad K. Sangma") are successfully matched or flagged.

---

## 20. Acceptance Criteria
* Multi-term profiles display consecutive terms correctly.
* Asset declarations list movable and immovable properties separately.
* Original affidavit PDFs load on demand.

---

## 21. Limitations
* Inconsistent scan qualities on older PDF files (prior to 2009) can cause OCR parsing errors.
* Unofficial party switching (outside assembly records) is not tracked.

---

## 22. Future Work
* Integrating assembly voting history and legislative attendance indicators.
* Automating political party metadata updates using official election notifications.

---

## 23. Related Documents
* [RELATIONAL_SCHEMA.md](file:///c:/python/LokTathya/docs/documents/data-model/RELATIONAL_SCHEMA.md)
* [VALIDATION_RECONCILIATION.md](file:///c:/python/LokTathya/docs/documents/data-quality/VALIDATION_RECONCILIATION.md)
