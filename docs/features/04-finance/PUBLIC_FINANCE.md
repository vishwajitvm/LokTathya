# Public Finance Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Public Finance Specification |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | Financial Allocation & Expenditure |

---

## 1. Overview
This document specifies the public finance data structures, municipal budget models, and audit reconciliation systems of the LokTathya platform. It details how financial data is ingested, verified, and mapped to geographic entities and public projects.

---

## 2. Problem Statement
Public financial data in India is published in inconsistent formats, often combining capital and revenue budgets across different accounting structures. Discrepancies between Budget Estimates (BE), Revised Estimates (RE), and Actuals (A) make it difficult to evaluate real utilization rates. We must build a database schema that models these structures and enforces audit trails back to the source documents.

---

## 3. Goals
* **Budget Tracking**: Map allocations, disbursals, and expenditures across fiscal years.
* **Deterministic Math**: Use pre-defined database equations to calculate utilization and variance rates.
* **Audit Trails**: Ensure all transaction figures are linked back to their original source document in the registry.

---

## 4. Non-Goals
* Running probabilistic forecasting models or using LLMs to perform financial arithmetic.

---

## 5. Target Users
* **Citizens & Taxpayers**: Monitor municipal expenditures and fund utilization in their cities.
* **Researchers**: Analyze public expenditure trends across states.
* **Journalists**: Investigate budget variances and underutilized funds.

---

## 6. User Stories
* As a citizen, I want to compare the capital expenditure allocation for public health in my city across the last three budgets.
* As a researcher, I want to download standardized JSON files containing budget items and audited actuals for a specific municipality.

---

## 7. User Journey
1. **Navigate**: The user opens the `/finance` dashboard.
2. **Select Entity**: The user selects a state, district, or city corporation.
3. **Audit**: The user reviews the overall funding utilization and inspects individual budget items by category (e.g. education, sanitation).

---

## 8. Functional Requirements
* **Standard Accounting Classifications**: Support revenue and capital expenditures.
* **Budget Stage Tracking**: Track figures across different budget stages (Budget Estimate, Revised Estimate, Actuals).
* **Variance Calculations**: Calculate the variance between initial budget estimates and actual expenditures.

---

## 9. Data Requirements
* Detailed Demand for Grants sheets from state and central ministries.
* Annual Financial Statements from municipal corporations.
* Audit reports from the Comptroller and Auditor General (CAG).

---

## 10. Backend Requirements
* **Deterministic Calculations**: Budget variance and utilization rates must be calculated in Python or SQL, not by LLMs:

$$\text{Utilization Rate} = \left( \frac{\text{Actual Expenditure}}{\text{Budget Allocation}} \right) \times 100$$

$$\text{Budget Variance} = \left( \frac{\text{Actual Expenditure} - \text{Budget Estimate}}{\text{Budget Estimate}} \right) \times 100$$

---

## 11. API Requirements
* `GET /api/v1/finance/budgets`: Retrieve budget summaries.
* `GET /api/v1/finance/items`: Retrieve individual budget items.

---

## 12. Frontend Requirements
* Interactive charts (bar, area) showing spending trends over time.
* Table structures displaying budget stages (BE, RE, Actuals) side-by-side.

---

## 13. Responsive Requirements
* **Mobile**: Simplified tables. Detailed breakdowns expand into collapsible sections.
* **Desktop**: Full grid layouts with charts and export capabilities (CSV, JSON).

---

## 14. Provenance Requirements
Every financial figure must contain a `source_id` pointing to its source document (e.g., `SRC-IN-MOF-001` Ministry of Finance sheets) in the registry.

---

## 15. Security Requirements
* **Access Control**: Administrative changes to financial records require authorized credentials.
* **Network Isolation**: Financial databases are hosted on private container networks.

---

## 16. Error Handling
* **Zero Denominator Handling**: If budget allocations are zero, the utilization rate calculation defaults to `0.0` or returns a null indicator instead of failing.

---

## 17. Data Quality
The ingestion task verifies that the sum of individual budget items matches the declared total.

---

## 18. Performance
Queries are indexed to ensure budget sheets load in under 50ms.

---

## 19. Testing
Unit tests verify that budget variance and utilization rate calculations are accurate.

---

## 20. Acceptance Criteria
* Financial calculations are deterministic.
* All figures link back to verified source files in the registry.
* Ingestion tasks validate math constraints before loading records.

---

## 21. Limitations
* Inconsistencies in accounting codes across municipal corporations make it difficult to standardize some budget items.
* Audit reports are often published with a two-year lag, delaying updates to actual expenditure data.

---

## 22. Future Work
* Integrating state-level accounting system APIs for automated budget data updates.
* Correlating budget allocations with demographic data to evaluate spending per capita.

---

## 23. Related Documents
* [RELATIONAL_SCHEMA.md](file:///c:/python/LokTathya/docs/documents/data-model/RELATIONAL_SCHEMA.md)
* [DETERMINISTIC_METRICS.md](file:///c:/python/LokTathya/docs/documents/analytics/DETERMINISTIC_METRICS.md)
