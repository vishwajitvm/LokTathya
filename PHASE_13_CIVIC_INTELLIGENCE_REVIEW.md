# PHASE 13 CIVIC INTELLIGENCE REVIEW

## Architecture Overview
The Civic Intelligence and Comparison Engine explicitly establishes a rigid, deterministic analysis layer. It completely walls off LLMs from manufacturing subjective metrics like "best representative" or "leadership scores", enforcing purely factual comparisons rooted in verifiable database rows.

## Attribution & Neutrality Policies
- **Neutral Language**: The system forbids inflammatory financial labels (`fraud`, `missing money`) for factual data gaps, instead employing terms like `unreconciled_amount` or `data_discrepancy`.
- **Project Attribution**: Geographic coincidence is explicitly isolated from causal attribution. A Representative's term overlapping with a Project's construction is displayed as a neutral temporal/spatial fact, NOT as political achievement unless specifically proven by an official document.

## Report Generation & Reproducibility
The `/api/v1/reports` endpoint generates immutable, snapshot-backed intelligence reports. Each report recursively binds the exact `content_version` IDs and `metric_definitions` utilized during its generation, ensuring 100% computational reproducibility years into the future.

## Data Origin Integrity
Every intelligence payload internally tracks its `data_origin` (`OFFICIAL_SOURCE`, `SYNTHETIC`). The API structurally prohibits synthetic architectural testing data from ever rendering as authoritative public civic facts on the frontend.

## Conflict Handling Integration
Building on Phase 9A, the comparison engine identifies unreconciled `CONFLICTING` observations and visually halts the comparison, injecting a "CONFLICTED DATA - REQUIRES REVIEW" block into the payload rather than silently picking an average.

## STOP CONDITION
The deterministic Civic Intelligence layer, Report API, and Frontend scaffolding are complete. No political scoring algorithms or predictive capabilities were introduced. 
Execution is stopped. Awaiting review.
