# Intelligence Reports Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Intelligence & Analytics Specification |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | Analytical Reports & Comparison Systems |

---

## 1. Purpose
This document specifies the analytical reports compilation, comparative indicators, snapshot versioning, and neutrality standards of the LokTathya platform.

---

## 2. Report Building & Reproducibility

Analytical reports (such as constituency profiles) compile multi-dimensional datasets to present trends over time:
* **Factual Focus**: Reports compile verified statistics (e.g. project completion rates, attendance rates) without qualitative grading.
* **Snapshot Versioning**: Reports are linked to the specific database snapshot version used to compile them. This ensures that historical reports remain consistent even as the database is updated with new records.
* **Snapshot Storage**: Generated PDF files are cached in MinIO under the `reports/` bucket and linked via the `reports` table.

---

## 3. Political Neutrality Standards

LokTathya maintains a strictly neutral stance:
* **Neutral Compilation**: We display raw, verified figures without commentary.
* **No Subjective Scoring**: The platform does not calculate "best/worst legislator" scores or qualitative ratings.
* **Data Discrepancies**: Conflicting records are displayed side-by-side with warning flags rather selecting one option arbitrarily.

---

## 4. Dossier Compilation Templates

The reporting system defines standard templates for exports:
* **Constituency Dossier**: Contains maps, list of active projects, historical election turnouts, and details of current representatives.
* **Representative Dossier**: Tracks attendance rate timelines, list of questions asked, and asset/liability disclosures.
* **Audit Dossier**: Compiles municipal financial line items and notes budget variances across fiscal years.

---

## 5. Neutral Language Guidelines

To prevent bias, the interface and generated reports must comply with these phrasing rules:
* **Action Verbs**: Use direct, objective verbs (e.g., *"represented"* or *"declared"*) rather than subjective terms (*"failed to attend"* or *"underperformed"*).
* **Factual Citing**: Direct references to source IDs are embedded directly in statements rather than presenting figures as general consensus.

---

## 6. Discrepancy Auditing & Comparison Controls

When comparing representatives or municipal budgets, the comparison engine enforces data checks:
* **Mismatched Fiscal Periods**: If a user attempts to compare two municipal budgets with different start months, the interface displays a warning explaining the formatting difference.
* **Partial Reporting Disclaimers**: If a representative's attendance data is missing for a session, the report excludes the period and adds an explanatory footnote instead of assuming zero participation.

---

## 7. Automated Dossier Caching & Expiry Cycles

Because database tables are modified during nightly ingestion batches, report metadata is cached with expiry limits:
* **Cache Storage**: Dossier metadata runs are cached in Redis under `report:cache:<id>` keys.
* **Expiry Trigger**: The system invalidates all cached reports for a constituency when a new data source mapping to that boundary is validated and reconciled.

---

## 8. Peer Verification & Public Dissemination Rules

* **Verification Badges**: Dossier files that have undergone dual administrator validation are marked with a `PEER_VERIFIED` badge on the web interface.
* **Public Sharing Metadata**: Exported reports include canonical OpenGraph meta headers, allowing citizens to share reports on social platforms with accurate previews.

---

## 9. Report Export Metrics & Logs

To monitor export usage and prevent system abuse:
* **Daily Export Limits**: Unauthenticated users are restricted to a maximum of 5 PDF downloads per day.
* **Export Audit Logs**: The backend records the target constituency ID, export timestamp, and IP address range in the `dossier_downloads_log` table.

---

## 10. Dossier Formatting Rules & Print Styles

* **CSS Print Styling**: Generated reports use clean CSS print rules (e.g., `@page` margins, page-break-inside properties) to prevent orphan headings and ensure tables do not cut off across pages in the exported PDF.
* **Footer Page Numbers**: Every page includes the compiled date and active page number (`Page X of Y`) to maintain a clean document flow.

---

## 11. PDF Output Page Budgeting Controls

To ensure dossiers fit clean page layouts:
* **Page Budgeting Engine**: The compiler scans document height, dynamically shrinking font sizes or line heights slightly if content overflows a page boundary by less than 10%.
* **Orphan Prevention**: Enforces a minimum of 3 trailing table rows per page, preventing solitary heading lines at page bottoms.

---

## 12. Automated PDF Quality Assurance

* **Render Checks**: The compilation worker validates PDF page count sizes. If a compiled PDF exceeds 100 pages, the compilation task is flagged as `COMPILATION_SIZE_EXCEEDED` to prevent memory lockups on the worker.
* **Metadata Attachment**: Reconciled files are stamped with signature metrics, confirming metadata verification before server distribution.
* **Security Scans**: The output engine checks the generated PDF structures to ensure no cross-site scripting strings are embedded in output templates.

---

## 13. Related Documents
* [REPORTS_GENERATION.md](file:///c:/python/LokTathya/docs/features/09-reports/REPORTS_GENERATION.md)
* [RESEARCH_WORKBENCH.md](file:///c:/python/LokTathya/docs/features/10-research/RESEARCH_WORKBENCH.md)
