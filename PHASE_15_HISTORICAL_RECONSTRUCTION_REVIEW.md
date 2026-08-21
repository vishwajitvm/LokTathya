# PHASE 15 HISTORICAL RECONSTRUCTION REVIEW

## Architecture Overview
The Historical Geography Engine (`backend/geography/historical.py`) enforces strict temporal boundary versioning. It structurally acknowledges that a constituency name does not guarantee a static geographic footprint across decades, explicitly mapping Delimitation Events (e.g., 2008) to PostGIS version boundaries.

## Geographic Comparability
The new `/api/v1/geographies/comparability` endpoint calculates comparability strictly via geometric intersection logic. It returns `NON_COMPARABLE` or `PARTIALLY_COMPARABLE` rather than silently allowing users to graph 1999 vote-shares directly against 2019 vote-shares for severely altered boundaries.

## Population Weighting Policy
In accordance with absolute rules, no arbitrary "population-weighted historical redistributions" were mathematically hallucinated. Because granular sub-ward historical population blocks are not available from verified sources, missing spatial overlays result in `NOT_COMPUTABLE` statuses.

## Entity Resolution
Historical Party names and Candidate identities are resolved using `sys_entity_resolution`. The engine preserves the raw original text from the ECI gazettes alongside the `canonical_id`, ensuring historical traceability without destroying the original source semantics.

## Forecasting Readiness Re-Evaluation
*Has Phase 15 sufficiently repaired historical depth and boundary continuity to support responsible forecasting?*

**Decision: PARTIALLY_READY**

**Evidence & Rationale:**
1. **Historical Depth**: Post-2008 delimited data now forms a solid 15-year contiguous block (2009-2024), satisfying the basic requirements for short-horizon baseline models (e.g., `Incumbency`).
2. **Boundary Discontinuity**: Pre-2008 data remains mathematically severed (`NON_COMPARABLE`) due to the 2008 Delimitation Commission boundary overhaul. Because LokTathya strictly prohibits inventing population weights to bridge this gap, pre-2008 elections cannot be robustly used as features for 2024 predictions.
3. **Model Eligibility**: We are `READY` to evaluate naive/deterministic historical baselines strictly within the post-2008 spatial boundaries. We remain `NOT_READY` for deep-time (30+ year) continuous statistical ML forecasting.

## STOP CONDITION
The temporal geography structures are implemented, historical boundary comparators are explicitly defined, and the API has been updated. No LLM prediction code or arbitrary forecasting metrics were generated. The stack remains fully Docker-containerized.

Execution is stopped. Awaiting review.
