# Deterministic Metrics Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Analytics Metrics Specification |
| Status | IMPLEMENTED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | Platform-Wide Analytics |

---

## 1. Purpose
This document specifies the deterministic metrics, mathematical formulas, and data validation rules used in the LokTathya platform. These metrics evaluate representative performance, project progress, and election dynamics without qualitative bias.

---

## 2. Metrics Registry

### A. Metric ID: `MET-FIN-001`
* **Name**: Constituency Fund Utilization Rate
* **Description**: Measures the percentage of released constituency development funds (MPLADS/MLACDF) that have been spent.
* **Formula**:

$$\text{Utilization Rate} = \left( \frac{\text{Spent Amount}}{\text{Released Amount}} \right) \times 100$$

* **Inputs**:
  * `Spent Amount` (Decimal, outstanding payments)
  * `Released Amount` (Decimal, disbursed funds)
* **Output**: Percentage (Decimal, 2 decimal places)
* **Unit**: `%` (Percentage)
* **Null Behavior**: Returns `null` if either the spent or released amount is missing.
* **Zero-Denominator Behavior**: If the released amount is zero, the utilization rate defaults to `0.00` to prevent division-by-zero errors.
* **Data Quality Requirements**: Disbursal records must be verified against MoSPI accounts.
* **Provenance**: Sanction orders from the Ministry of Statistics and Programme Implementation.
* **Version**: 1.0.0
* **Example**:
  * Spent = INR 4,00,00,000; Released = INR 5,00,00,000
  * Utilization = 80.00%
* **Test Case**:
  * Input: `{"spent": 40000000.00, "released": 50000000.00}` ➡️ Output: `80.00`

---

### B. Metric ID: `MET-FIN-002`
* **Name**: Budget Variance Rate
* **Description**: Measures the difference between initial budget estimates and actual expenditures.
* **Formula**:

$$\text{Budget Variance} = \left( \frac{\text{Actual Expenditure} - \text{Budget Estimate}}{\text{Budget Estimate}} \right) \times 100$$

* **Inputs**:
  * `Actual Expenditure` (Decimal, audited expenses)
  * `Budget Estimate` (Decimal, approved allocation)
* **Output**: Percentage (Decimal, 2 decimal places)
* **Unit**: `%` (Percentage, can be positive or negative)
* **Null Behavior**: Returns `null` if the budget estimate or actual expenditure is missing.
* **Zero-Denominator Behavior**: If the budget estimate is zero, the variance rate defaults to `0.00` or returns a null indicator.
* **Data Quality Requirements**: Figures must be sourced from audited annual accounts.
* **Provenance**: Audited accounts from the Comptroller and Auditor General (CAG).
* **Version**: 1.0.0
* **Example**:
  * Actual = INR 1,20,00,000; Estimate = INR 1,00,00,000
  * Variance = 20.00%
* **Test Case**:
  * Input: `{"actual": 12000000.00, "estimate": 10000000.00}` ➡️ Output: `20.00`

---

### C. Metric ID: `MET-REP-001`
* **Name**: Assembly Attendance Rate
* **Description**: Measures the percentage of legislative session days attended by a representative.
* **Formula**:

$$\text{Attendance \%} = \left( \frac{\text{Days Present}}{\text{Total Session Days}} \right) \times 100$$

* **Inputs**:
  * `Days Present` (Integer)
  * `Total Session Days` (Integer)
* **Output**: Percentage (Decimal, 2 decimal places)
* **Unit**: `%` (Percentage)
* **Null Behavior**: Returns `null` if attendance registers are missing.
* **Zero-Denominator Behavior**: If total session days is zero, the attendance rate defaults to `0.00` to prevent division-by-zero errors.
* **Data Quality Requirements**: Session registers must be verified against official assembly bulletins.
* **Provenance**: Session attendance registers from Parliament and State Assemblies.
* **Version**: 1.0.0
* **Example**:
  * Days Present = 18; Total Days = 20
  * Attendance = 90.00%
* **Test Case**:
  * Input: `{"present": 18, "total": 20}` ➡️ Output: `90.00`

---

## 3. Related Documents
* [PUBLIC_FINANCE.md](file:///c:/python/LokTathya/docs/features/04-finance/PUBLIC_FINANCE.md)
* [REPRESENTATIVE_PERFORMANCE.md](file:///c:/python/LokTathya/docs/features/06-performance/REPRESENTATIVE_PERFORMANCE.md)
