# Quarantine & Validation Policy
Multi-tier validation (Document, Schema, Domain, Geographic, Financial). Invalid records are quarantined in Postgres with explicit reason codes (`PARSER_ERROR`, `SCHEMA_ERROR`) allowing human inspection.
