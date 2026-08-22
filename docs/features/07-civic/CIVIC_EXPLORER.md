# Civic Explorer Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Public Interface Specification |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | Public Civic Search & Exploration |

---

## 1. Overview
This document specifies the Civic Explorer public search, discovery, and citation interface of the LokTathya platform. The Civic Explorer acts as the primary web application interface, enabling users to search, explore, and download verified Indian civic datasets.

---

## 2. Problem Statement
Accessing public civic data is often restricted by obscure search interfaces, lack of cross-references between related datasets, and missing links to original source documents. Citizens and researchers need a unified, search-driven web application to explore public records without getting lost in multiple government portals.

---

## 3. Goals
* **Search-Driven Discovery**: Provide a search interface resolving queries to matching representatives, constituencies, projects, or elections.
* **Traceable Context**: Present related datasets side-by-side (e.g. mapping a representative to their constituency's project portfolio).
* **Transparent Citations**: Ensure every database record displayed on the frontend includes a citation block linking to the original source.

---

## 4. Non-Goals
* Providing real-time news feeds, hosting political discussion forums, or publishing editorial commentary.

---

## 5. Target Users
* **Citizens & Voters**: Explore local representatives, candidates, and development projects.
* **Researchers & Academics**: Search and compile historical civic datasets for studies.
* **Journalists**: Find and verify candidate disclosures and municipal financial records.

---

## 6. User Stories
* As a citizen, I want to search for my town name and see my current Parliamentary constituency, MP, and active road projects.
* As a researcher, I want to inspect the source registry citation for a representative's asset declaration to confirm its authenticity.

---

## 7. User Journey
1. **Search**: The user enters a search query (e.g., "Conrad Sangma" or "Shillong") on the `/search` page.
2. **Explore**: The user selects a search result (e.g., a representative profile or constituency map).
3. **Audit**: The user reviews the details page, navigating between tabs for performance, projects, and elections.
4. **Citation**: The user clicks a citation block to view the original government PDF document.

---

## 8. Functional Requirements
* **Constituency Search**: Search for constituencies by name or location.
* **Representative Profiles**: Show candidate history, multi-term details, and disclosures.
* **Project Maps**: Display active public works projects on the constituency map.
* **Source Registry Citations**: Embed clickable citation links on all public record cards.

---

## 9. Data Requirements
* Indexes of representatives, constituencies, elections, and projects from core database tables.
* Source metadata and storage paths from the `sources` registry table.

---

## 10. Backend Requirements
* **Fuzzy Search API**: Uses PostgreSQL full-text search indexes to resolve candidate spelling variations.
* **Citation Resolution API**: Resolves internal source IDs to direct PDF download URLs.

---

## 11. API Requirements
* `GET /api/v1/search/`: Resolves queries to matching database records.
* `GET /api/v1/search/suggestions`: Returns auto-complete suggestions.

---

## 12. Frontend Requirements
* Clean, search-centric layout on the homepage.
* Standardized `Citation` components showing the source registry ID and download link.

---

## 13. Responsive Requirements
* **Mobile**: Single-column layout. Search filters collapse into a drawer interface.
* **Desktop**: Grid layout with side-by-side search filters and suggestions.

---

## 14. Provenance Requirements
Every public record card displayed on the frontend must embed a `Citation` component linking to the source.

---

## 15. Security Requirements
User search queries are processed in-memory and are not persisted in database logs to protect user privacy.

---

## 16. Error Handling
* **No Search Results**: Displays an empty search state page suggesting spelling corrections or alternate terms.
* **Missing Source File**: If a source PDF is unavailable, the citation links show a `FILE_NOT_FOUND` status.

---

## 17. Data Quality
The search engine indexes are updated dynamically during data ingestion runs to ensure search results reflect database records.

---

## 18. Performance
* Search results are cached in Redis to keep response times under 20ms.
* API responses are paginated to optimize rendering performance on large datasets.

---

## 19. Testing
Unit tests verify that search queries successfully resolve to the correct representatives or constituencies.

---

## 20. Acceptance Criteria
* Search results load in under 20ms for cached queries.
* Clickable citation links are present on all public record cards.
* Auto-complete suggestions are accurate.

---

## 21. Limitations
* Spelling variations in user queries can occasionally return irrelevant results, requiring improved fuzzy search parameters.
* Scanned PDF documents cannot be searched via full-text search indexes.

---

## 22. Future Work
* Integrating multilingual search capabilities (e.g. Hindi, regional languages).
* Correlating search trends with demographic data to identify popular civic issues.

---

## 23. Related Documents
* [API_REFERENCE.md](file:///c:/python/LokTathya/docs/documents/api/API_REFERENCE.md)
* [DESIGN_SYSTEM.md](file:///c:/python/LokTathya/docs/documents/design/DESIGN_SYSTEM.md)
