# Chunking Policy
Avoid arbitrary fixed-token splits. Rely on `DocumentChunker` to respect PDF outlines, headings, tables, and paragraphs.
Chunks MUST retain `document_id`, `content_version_id`, `page_number`, and `section`.
