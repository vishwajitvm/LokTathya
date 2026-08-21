# Forecasting Readiness Policy
LokTathya does NOT deploy predictive models merely because the code executes.
Readiness is gated by the `ForecastingReadinessEngine`, which measures boundary continuity, missing result thresholds, and historical depth (minimum 10+ years of comparable data).
