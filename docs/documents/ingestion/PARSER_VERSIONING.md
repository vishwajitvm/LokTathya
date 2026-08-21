# Ingestion Factory Architecture
The Operational Ingestion pipeline runs verified sources through a strict Batch architecture. 
Failure isolation ensures that a parser failure on Source C does not halt the canonicalization of Source A and B.
