# AI Policy

## Political Neutrality
- LokTathya is an information and civic-data infrastructure project, not a political persuasion platform.

## Evidence-Backed AI
- AI must distinguish between OFFICIAL FACT, DERIVED VALUE, MODEL-GENERATED, COMMUNITY-REPORTED, UNKNOWN.
- Every factual answer must include evidence/citations.
- Never fabricate citations.

## Model Utilization
- Do NOT send the entire database to an LLM.
- Numerical questions should use SQL via calculation engine, not LLM arithmetic guessing.

## Embedding Policy
- Embed: government documents, policy circulars, audit/tender reports, long text.
- Do NOT embed: IDs, raw numerical facts, project amounts, election votes, dates, administrative IDs.

## Fallback
- Robust model/provider/local fallback mechanisms must be in place.
