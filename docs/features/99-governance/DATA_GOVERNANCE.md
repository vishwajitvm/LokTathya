# Data Governance & Ethics Policy

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Governance Policy Specification |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | Global Data Governance |

---

## 1. Overview
This document specifies the data governance framework, source verification protocols, privacy safeguarding models (PII scrubbing), political neutrality guidelines, and AI safety constraints of the LokTathya platform. It defines the principles that govern how the platform handles public data and maintains neutrality.

---

## 2. Problem Statement
Aggregating civic and political records involves handling sensitive data, including candidate disclosures and municipal financial allocations. Presenting this data in biased ways or failing to redact personal contact details can lead to security, privacy, and neutrality concerns. We must establish a clear data governance policy to ensure transparency, neutrality, and user privacy.

---

## 3. Goals
* **Strict Neutrality**: Ensure all political parties, candidates, and legislatures are treated equally and objectively.
* **PII Redaction**: Automatically identify and redact private contact details from public affidavits.
* **Traceable Provenance**: Link every database record to an official source document in the registry.

---

## 4. Non-Goals
* Publishing political commentary, taking editorial stances, or rating candidates' character.

---

## 5. Target Users
* **Data Contributors**: Learn about contribution guidelines and data quality requirements.
* **System Auditors**: Verify compliance with privacy regulations and security policies.
* **Public Users**: Understand how the platform collects, handles, and protects civic data.

---

## 6. User Stories
* As a user, I want to be confident that the platform does not collect or track my personal search queries or location coordinates.
* As a contributor, I want clear guidelines on how to format database schemas and handle conflicting data sources.

---

## 7. User Journey
1. **Explore**: A user accesses the platform to search for civic records.
2. **Review**: The user reads the privacy policy and disclaimer pages to understand the platform's constraints and neutrality stance.
3. **Contribute**: A developer inspects the contribution guidelines to submit new data schemas or connectors.

---

## 8. Functional Requirements
* **Audit Trail Tracking**: Every database record must include fields for creation time, update time, and the source registry ID.
* **PII Redaction Workflow**: Regex filters scan text fields to identify and redact PAN cards, phone numbers, and bank details.
* **Conflict Flagging**: Discrepancies between official sources must be logged as conflicts and routed to the admin review queue.

---

## 9. Data Requirements
* Source documents must be obtained from official archives (e.g. ECI, Survey of India, Ministry of Finance).
* Personal contact details must be redacted during the ingestion process before saving to the database.

---

## 10. Backend Requirements
* **Redaction Pipeline**: Celery workers run regex parsing filters on all text extractions:
  * **PAN Card Regex**: `[A-Z]{5}[0-9]{4}[A-Z]{1}`
  * **Phone Numbers**: Scrubbed using country-specific phone patterns.
  * **Bank Account Details**: Redacted using IFSC and account number patterns.
* **Reconciliation Engine**: Logs conflicting inputs in `data_quality_conflicts` for review.

---

## 11. API Requirements
* `GET /api/v1/data-quality/conflicts`: Retrieve active database discrepancies.
* `POST /api/v1/data-quality/resolve`: Administrative endpoint to resolve conflicts.

---

## 12. Frontend Requirements
* Display clear warning flags on records with active database conflicts.
* Link to the privacy policy, disclaimer, and terms of use pages in the global footer.

---

## 13. Responsive Requirements
* **Mobile**: Warning flags and disclaimers are prominently displayed above content cards.
* **Desktop**: Full audit logs and conflict descriptions are visible in side panels.

---

## 14. Provenance Requirements
Every public record must link back to its verified source file in the registry (e.g. `SRC-IN-ECI-001` nomination affidavits).

---

## 15. Security Requirements
* **Network Isolation**: Databases reside strictly inside the private Docker network `loktathya_net`.
* **Access Control**: Administrative operations require authorized credentials.

---

## 16. Error Handling
* **Unresolved Conflicts**: If a conflict is unresolved, both records remain visible to the public with a disclaimer flag rather than selecting one arbitrarily.

---

## 17. Data Quality
The reconciliation engine validates that all imported data complies with data quality and schema constraints before clearing records.

---

## 18. Performance
PII redaction and conflict mapping are processed asynchronously by Celery workers to avoid impacting API response times.

---

## 19. Testing
Unit tests verify that regex filters successfully identify and redact PAN card patterns and phone numbers.

---

## 20. Acceptance Criteria
* The platform presents data neutrally.
* Private PII is successfully redacted.
* Conflicting data is logged as a conflict and not silently resolved.

---

## 21. Limitations
* Variations in handwritten text scans can occasionally limit the accuracy of automated PII redaction, requiring manual review.
* Reconciling conflicting data from state and central portals can take time, delaying updates to database records.

---

## 22. Future Work
* Integrating machine learning-based entity recognition models to improve PII detection accuracy.
* Automating conflict notification emails to project maintainers when discrepancies are logged.

---

## 23. Related Documents
* [VALIDATION_RECONCILIATION.md](file:///c:/python/LokTathya/docs/documents/data-quality/VALIDATION_RECONCILIATION.md)
* [SOURCE_CATALOG.md](file:///c:/python/LokTathya/docs/documents/source-registry/SOURCE_CATALOG.md)
