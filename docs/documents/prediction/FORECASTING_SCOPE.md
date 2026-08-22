# Forecasting Scope Specification

| Field | Value |
|---|---|
| Project | LokTathya |
| Document Type | Predictive Analytics Scope Specification |
| Status | PLANNED |
| Version | 1.0.0 |
| Last Updated | 2026-08-22 |
| Owner | LokTathya Project |
| Scope | Forecasting & Predictive Analytics Subsystem |

---

## 1. Purpose
This document specifies the scientific boundaries, backtesting guidelines, and limitations for predictive analytics and forecasting in the LokTathya platform.

---

## 2. Background & Status
* **Status**: `PLANNED`
* **Notes**: LokTathya currently does **not** host active forecasting models or election predictions. This document establishes the guidelines for when these features are developed.

---

## 3. Ethical Forecasting Guidelines

**Predictive analytics** (such as modeling election outcomes or project completion delays) can be misinterpreted as definitive facts. We establish these rules:

1. **Explicit Limitations**: All predictive dashboards must display clear disclaimers explaining that predictions are based on historical models and are not statements of fact.
2. **Explainability**: Models must output confidence intervals (e.g. 95% confidence bounds) and list the primary features used to generate the forecast.
3. **No Direct LLM Predictions**: Large Language Models must not be used to forecast election outcomes or project budgets. Predictions must use verified statistical models (e.g. regression models).

---

## 4. Baseline Models & Evaluation Metrics

When forecasting features are developed, they must use verified baseline models:
* **Baseline Selection**: Simple historical trend lines or regression models must be used as baselines before adopting complex machine learning models.
* **Evaluation Metrics**: Models must be evaluated using standard metrics:
  * **Mean Absolute Error (MAE)** for budget timelines and expenditures.
  * **F1-Score** for categorical outcomes (e.g., project completion flags).

---

## 5. Backtesting & Leakage Prevention

When predictive features are developed, they must comply with the following validation checks:
* **Temporal Splits**: Training and testing datasets must be split temporally (e.g., training on pre-2019 elections and testing on 2024 elections) to prevent future data leakage.
* **Leakage Audits**: Feature sets are audited to ensure they do not incorporate information that would be unavailable at the time of the forecast.

---

## 6. Feature Registry & Data Continuity

To ensure reproducibility, all features used by models must be documented in a central feature registry:
* **Feature ID**: Unique identifier (e.g., `FEAT-REP-ATTEND`).
* **Source Tracking**: Features must map to active table columns, ensuring the underlying raw data can be audited back to the source.
* **Geographical Continuity Check**: If boundary changes occur between elections, the feature generator must adjust input values based on overlap metrics to prevent spatial bias.

---

## 7. Model Bias Audit & Demographic Fairness Checks

To ensure model neutrality:
* **Bias Audits**: Models must be evaluated for demographic parity across geographic regions to prevent bias against rural or underrepresented districts.
* **Feature Weights Auditing**: The system must log model coefficients or feature importances to verify that demographic indicators (e.g. religion, caste) are excluded from forecasting features.

---

## 8. Backtesting Execution & Log Records

* **Log Registry**: Backtesting run parameters (epochs, split dates, MAE results, feature configurations) are recorded in the `backtest_runs` database table.
* **Model Validation Flags**: If a model's MAE exceeds historically observed limits, the model is flagged as `UNSTABLE` and blocked from rendering predictions in public user profiles.

---

## 9. Model Retraining Schedules

To keep prediction systems up-to-date:
* **Retraining Cycles**: Models are scheduled for automatic retraining after the completion of an election cycle or the publication of audited municipal accounts.
* **Release Approval Gates**: Updated models must exceed the historical F1-score baseline by at least `0.05` before being pushed to production.

---

## 10. Data Drift Audits & Feature Refresh Timers

* **Drift Detection**: When new census or demographic datasets are loaded, the system automatically runs data drift audits using Kolmogorov-Smirnov statistical tests.
* **Feature Refreshes**: If significant data drift is identified, the system invalidates active forecasting runs and schedules immediate model retraining.

---

## 11. Uncertainty Visualizations in User Interfaces

To represent predictive limits clearly:
* **Confidence Shading**: Chart overlays displaying predictions must use shaded error boundaries representing standard deviations rather than single coordinate lines.
* **Disclaimer Headers**: Tooltips explain standard error terms to assist users in interpreting accuracy variations.

---

## 12. Model Registration & Deployment Registry

* **Model Registry Records**: Retrained and approved models are registered in the `forecasting_models` metadata registry, indicating parameter sets, model types, and target features.
* **Active Status Flags**: Only models with status `ACTIVE` are queried by the API endpoints, preventing deprecated configurations from serving outdated forecasts.
* **Rollback Capabilities**: Enables administrators to restore a previous model version instantly if data drift causes unexpected output values.

---

## 13. Related Documents
* [RESEARCH_WORKBENCH.md](file:///c:/python/LokTathya/docs/features/10-research/RESEARCH_WORKBENCH.md)
* [DETERMINISTIC_METRICS.md](file:///c:/python/LokTathya/docs/documents/analytics/DETERMINISTIC_METRICS.md)
