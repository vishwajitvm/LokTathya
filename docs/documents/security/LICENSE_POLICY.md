# LokTathya License & Attribution Policy

This document regulates the licensing compliance rules for civic datasets ingested and redistributed by LokTathya.

---

## 1. Metadata Mapping
Every Source record in the registry must explicitly state:
- `license`: e.g., OGD (Open Government Data), CC-BY-4.0, or proprietary/copyright-protected.
- `attribution`: The required text template referencing the authority and department of origin.
- `access_policy`: Standardized limits defining if the data can be fully cached, partially cached, or only indexed.

---

## 2. Permissive Data Use
- Datasets distributed under Open Government licenses (e.g. India OGD) are saved, parsed, and exposed through search and API queries without restrictions.
- In all API responses, the attribution metadata of the source is injected automatically under the `meta.provenance` block.

---

## 3. Restricted Document Content
- Official documents that are copyright-protected but publicly accessible are processed to extract structured canonical facts (e.g. numeric allocations) under fair-use principles.
- The raw source files (e.g. PDFs) of restricted documents are NOT served directly to public API consumers. Only the facts and links to the original government URL are exposed.

---

## 4. Citation Requirements
- The front-end must display citations alongside any derived metrics or summaries.
- A citation block contains:
  - Source department/agency name.
  - Document title and version number.
  - Original source URL and retrieval timestamp.
  - The hash index of the raw artifact in MinIO for verification.
