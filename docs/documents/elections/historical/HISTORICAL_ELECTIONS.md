# Historical Elections Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Election Domain Historical Specification |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | Historical Election Data & Delimitation Comparability |

---

## 1. Purpose
This document specifies the methodologies, database mappings, and limitations for reconstructing historical election records across boundary shifts and delimitation cycles in the LokTathya platform.

---

## 2. Background
Comparing election results over time is complicated by boundary shifts during delimitation cycles. When a constituency's physical borders are redrawn, the demographic composition and total registered voter counts shift, making direct comparisons of vote margins or party support between elections in different cycles inaccurate. We must establish a framework to map constituency continuity.

---

## 3. Delimitation & Comparability Models

[![Delimitation & Comparability Models](https://mermaid.ink/img/Zmxvd2NoYXJ0IFRCCiAgICBDeWNsZUFbRGVsaW1pdGF0aW9uIEN5Y2xlIEEgZS5nLiAxOTczXSAtLT4gUG9seWdvbkFbQ29uc3RpdHVlbmN5IEJvdW5kYXJ5IFBvbHlnb24gQV0KICAgIFBvbHlnb25BIC0tPiBJbnRlcnNlY3RbU3BhdGlhbCBJbnRlcnNlY3QgU1RfSW50ZXJzZWN0aW9uXQogICAgSW50ZXJzZWN0IC0tPiBPdmVybGFwW0NhbGN1bGF0ZSBPdmVybGFwICVdCiAgICBJbnRlcnNlY3QgLS0-IFBvbHlnb25CW0NvbnN0aXR1ZW5jeSBCb3VuZGFyeSBQb2x5Z29uIEJdCiAgICBQb2x5Z29uQiAtLT4gQ3ljbGVCW0RlbGltaXRhdGlvbiBDeWNsZSBCIGUuZy4gMjAwMl0=)](https://mermaid.ink/img/Zmxvd2NoYXJ0IFRCCiAgICBDeWNsZUFbRGVsaW1pdGF0aW9uIEN5Y2xlIEEgZS5nLiAxOTczXSAtLT4gUG9seWdvbkFbQ29uc3RpdHVlbmN5IEJvdW5kYXJ5IFBvbHlnb24gQV0KICAgIFBvbHlnb25BIC0tPiBJbnRlcnNlY3RbU3BhdGlhbCBJbnRlcnNlY3QgU1RfSW50ZXJzZWN0aW9uXQogICAgSW50ZXJzZWN0IC0tPiBPdmVybGFwW0NhbGN1bGF0ZSBPdmVybGFwICVdCiAgICBJbnRlcnNlY3QgLS0-IFBvbHlnb25CW0NvbnN0aXR1ZW5jeSBCb3VuZGFyeSBQb2x5Z29uIEJdCiAgICBQb2x5Z29uQiAtLT4gQ3ljbGVCW0RlbGltaXRhdGlvbiBDeWNsZSBCIGUuZy4gMjAwMl0=)

### A. Spatial Overlap Calculations
To compare constituencies across delimitation cycles, the database calculates boundary overlaps using PostGIS:

$$\text{Overlap \%} = \left( \frac{\text{Area}(\text{Boundary A} \cap \text{Boundary B})}{\text{Area}(\text{Boundary A})} \right) \times 100$$

* **High Comparability (Overlap >= 90%)**: The constituency is considered continuous. Historical results can be compared directly.
* **Partial Comparability (50% <= Overlap < 90%)**: The constituency is marked as partially comparable with a disclaimer explaining the boundary shift.
* **Low Comparability (Overlap < 50%)**: Direct comparisons are blocked.

---

## 4. Candidate & Party Identity Resolution

* **Fuzzy Candidate Resolution**: Matches candidate profiles across elections using name spelling variation indexes.
* **Party Splitting & Merger Timelines**: Tracks changes in party affiliations (e.g. when a party splits into factions), ensuring vote totals are correctly attributed to their historical organizations rather than modern party structures.

---

## 5. Temporal Mapping & Voter Reconstitution

When boundaries shift, mapping demographic patterns requires allocating registered voters proportionally based on overlap areas:

$$\text{Estimated Voters} = \text{Registered Voters (Polygon A)} \times \left( \frac{\text{Area}(\text{Boundary A} \cap \text{Boundary B})}{\text{Area}(\text{Boundary A})} \right)$$

* **Neutrality Guidelines**: Calculated results are flagged as `ESTIMATED_POPULATION` to distinguish them from direct election counts.
* **Redistribution Checks**: Reconstitution math checks ensure that the sum of estimated voters across split boundaries equals the original total.

---

## 6. Political Party Chronology Registry

To prevent historical misattributions, the database maps political parties to a timeline table:
* **Splits**: Tracks splits (e.g. when a party splits into two new organizations) and assigns voter shares to the faction that carried the name.
* **Mergers**: Tracks party mergers and handles shifts in candidates' declared parties across election cycles to maintain analytical continuity.

---

## 7. Independent Candidates & Party Symbols

* **Independent Matching**: Candidates running as Independents (IND) are mapped using unique identifiers matching their district and year, preventing the merging of different independent candidates with identical names.
* **Electoral Symbol Tracking**: Tracks changes in party symbols (e.g., hand, lotus, bicycle) between election cycles to ensure visual and data continuity.

---

## 8. Ingestion Constraints on Historic Turnout Data

When importing older election results:
* **Missing Gender Breakdowns**: If turnout details by gender are missing in historical files, the record is flagged, leaving gender specific fields as `NULL` instead of projecting values.
* **Write-in Candidate Validation**: Tracks and reconciles changes in candidate listings when political groups are banned or boycotted.

---

## 9. Delimitation Boundary Overlaps Verification Checklist

Every spatial boundary change must be validated against the checklist before release:
* **Topology Overlap Verifications**: Confirms that area calculations do not produce negative regions.
* **Spatial Join Indexes**: Verifies that the spatial joins link all historical candidates within the redrawn district boundaries.

---

## 10. Independent Election Commission Oversight Reviews

To ensure maximum accuracy:
* **Oversight Logs**: Reconciled historical boundaries undergo review by GIS data analysts.
* **State Archives Alignment**: Verification audits cross-check coordinate boundaries against the text definitions published in CEO reports.

---

## 11. Related Documents
* [ELECTION_ANALYTICS.md](file:///c:/python/LokTathya/docs/features/05-elections/ELECTION_ANALYTICS.md)
* [HISTORICAL_GEOGRAPHY.md](file:///c:/python/LokTathya/docs/documents/geography/historical/HISTORICAL_GEOGRAPHY.md)
