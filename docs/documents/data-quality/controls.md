# Data Quality Controls & Reconciliation Engine

This document details the validation, normalization, and entity resolution strategies implemented in Phase 5 of LokTathya.

---

## 1. Type Normalization
We employ deterministic matching rules to clean and unify heterogeneous raw values:
- **Numeric Normalizer**: Converts text figures to decimals, handling Indian units (lakh = $10^5$, crore = $10^7$), removing Rupees signs (₹, Rs.), wrapping negative formats (e.g., `(4,500)` -> `-4500`), and resolving percentage divisions.
- **Temporal Normalizer**: Recognizes ISO standard formats, Indian date structures (`DD-MM-YYYY`), and periods (like `2024-25` representing financial years from April 1st to March 31st).

---

## 2. Entity Resolution Matchers
- **Exact & Alias Mappings**: Queries system-registered mappings to match known entities.
- **Fuzzy Sequence Matching**: Matches spelling variations (e.g. Narendra Modi vs N. Modi) using difflib ratios.
- **Geographic Constraints**: Rejects match candidates if parent containment checks do not align, routing mismatching rows to human review queues.

---

## 3. Reconciliation Rules
If multiple official observations relate to the same canonical fact:
- If the publication dates differ, the newer observation supersedes the older value.
- If the values match, they are marked as **CONSISTENT**.
- If the values differ but dates are identical or unknown, they are marked as **CONFLICTING** and flagged for human review.
