# Citation Validation
The `CitationValidator` ensures no factual claims exit the API without exact alignment to the `evidence_set`.
If the LLM hallucinates a number not supplied by the tools, the response block is stripped or re-generated.
