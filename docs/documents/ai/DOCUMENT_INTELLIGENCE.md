# Document Intelligence Architecture
LokTathya distinguishes clearly between Authoritative Facts (SQL), Document Content (Full Text/Vector), and AI-Generated Responses.
All extraction, OCR, and embedding pipelines strictly feed the `ai_chunk` and `ai_embedding` storage architectures without mutating canonical raw facts.
