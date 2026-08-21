# PHASE 9A DATA QUALITY REVIEW

## Conflict Types & Resolution Strategy
The `ReconciliationEngine` explicitly segregates raw `observations` from the final `canonical` tables.
Differences in reported facts (e.g., Financial Amounts, Project Statuses) are routed into conflict statuses: `CONSISTENT`, `MINOR_VARIANCE`, `CONFLICTING`, `SUPERSEDED`, and `UNRESOLVED`. 
If an observation is explicitly a newer chronological revision, it is marked `SUPERSEDED`, preserving history while updating canonical state.

## AI Behavior
LLMs are STRICTLY prohibited from resolving data conflicts. The prompt injection layers and chat logic are bound to surface unresolved conflicts transparently rather than hallucinating an average or picking a source arbitrarily.

## Provenance Behavior
When a canonical fact is derived from multiple observations, the engine attaches a provenance mapping to both the selected observation and the superseded/conflicting observations, making disagreements fully visible to the `api/v1/data-quality/conflicts` endpoint.

## Metric Safety
The analytics engine respects `CONFLICTED` statuses by throwing `INSUFFICIENT_DATA` rather than returning high-confidence metric calculations over disputed numerical baselines.

## Known Limitations
- Determining `SUPERSEDED` state requires strict Date constraints from government documents, which are often missing or ambiguous (e.g. "2024-25" vs a hard timestamp).
- Source Authority routing (e.g., Election Commission > Ministry of Finance for candidate identity) requires rigorous domain-mapping tables yet to be fully populated.

## STOP CONDITION
The foundational conflict reconciliation layer is complete. Data is never silently overwritten, and LLMs are stripped of truth-adjudication power. No mass ingestion was executed.
Execution is stopped. Awaiting review.
