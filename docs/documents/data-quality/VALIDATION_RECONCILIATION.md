# Validation & Reconciliation Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Data Quality Specification |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | Data Quality & Reconciliation Subsystem |

---

## 1. Purpose
This document specifies the validation rules, entity reconciliation engine, confidence scoring configurations, and quarantine states of the LokTathya platform. It details how data discrepancies and duplicates are resolved during ingestion runs.

---

## 2. Ingestion & Data States

All imported data passes through a series of validation stages to ensure accuracy before being loaded into core tables:

```
[Raw Document] ---> [Parsed Data] ---> [Normalized Data] ---> [Validated Data]
                                                                     |
                                                                     v
[Canonical Database] <--- (Resolve) <--- [Reconciliation Engine] <--- (Match)
```

1. **RAW**: The raw file is uploaded to MinIO and registered in the `sources` table with a unique cryptographic hash to ensure auditability.
2. **PARSED**: The document text is extracted and structured.
3. **NORMALIZED**: Translates values (e.g. spelling aliases, currency variations) into standard formats.
4. **VALIDATED**: Math checks (e.g., verifying that the sum of votes matches the constituency total) are executed. Mismatches are routed to the **Quarantine** database.
5. **RESOLVED**: Fuzzy name matching is run against existing database profiles.
6. **CANONICAL**: Reconciled data is loaded into the core database tables.

---

## 3. Fuzzy Name Resolution & Confidence Scoring

During representative ingestion runs, names can contain spelling variations. The reconciliation engine uses Levinshtein fuzzy matching logic to calculate similarity scores:

* **Score >= 0.90**: Automated merge. The record is linked to the existing profile.
* **0.75 <= Score < 0.90**: Ambiguity flag. The record is logged as a conflict in the `data_quality_conflicts` table for manual review.
* **Score < 0.75**: New entity. A new representative profile is generated.

### Fuzzy Matching Calculation Example:
The Levinshtein ratio is calculated as:

$$\text{Similarity Ratio}(S_1, S_2) = \frac{|S_1| + |S_2| - \text{LevenshteinDistance}(S_1, S_2)}{|S_1| + |S_2|}$$

* For name profiles: `S1 = "Conrad Sangma"`, `S2 = "Conrad K. Sangma"`.
* Ratio evaluates to `0.88`, placing the record in the ambiguity range (logged as conflict for review).

---

## 4. Conflict Resolution Panel & Audit Overrides

Discrepancies identified during validation (e.g. conflicting asset declarations between state and central portals) are routed to the admin conflict resolution queue:
* **Pending Stage**: The record remains flagged as `DATA_DISCREPANCY` (Pending Review).
* **Audit Resolution**: Project maintainers inspect the original source PDFs and choose to:
  * Approve one of the records and update the database.
  * Keep both options visible with a disclaimer flag to inform the public.
* **Manual Override Log**: When an administrator forces a reconciliation resolution (e.g. merging two profiles manually), the system creates an entry in `administrative_overrides` logging the user ID, timestamp, and justification.

---

## 5. Validation Rules & Math Constraints

The system runs several automated checks on incoming files:
* **Elections Validation**: Total votes cast for all candidates must not exceed the total registered voters.
* **Finance Validation**: The sum of all budget line items must match the declared total expenditure for the fiscal year.
* **Asset Validation**: Movable assets plus immovable assets must equal the total declared candidate assets.
* **Quarantine Actions**: If a validation check fails, the record is flagged, marked as `FAILED_VALIDATION`, and written to the quarantine registry to prevent bad data from polluting the production tables.

---

## 6. Quarantine Data Retention & Purge Rules

To prevent quarantine tables from consuming excessive database resources:
* **Retention Period**: Quarantined records and extraction logs are kept for a maximum of 90 days.
* **Automated Purging**: A weekly Celery Beat task identifies and removes quarantined logs older than 90 days if their status is marked as `RESOLVED` or `DISMISSED`.
* **Permanent Archive**: The original raw source files in the MinIO quarantine bucket are never deleted, ensuring the ability to audit historical runs.

---

## 7. Automated Model Calibration & Learning

When administrators resolve ambiguities:
* **Fuzzy Weight Tuning**: The Levinshtein threshold weights are dynamically adjusted in the database when overrides are logged to improve future automated matches.
* **Feedback Loops**: The system records the spelling corrections, automatically adding them to the global abbreviations register for future runs.

---

## 8. Related Documents
* [DATA_GOVERNANCE.md](file:///c:/python/LokTathya/docs/features/99-governance/DATA_GOVERNANCE.md)
* [INGESTION_PIPELINE.md](file:///c:/python/LokTathya/docs/documents/ingestion/INGESTION_PIPELINE.md)
