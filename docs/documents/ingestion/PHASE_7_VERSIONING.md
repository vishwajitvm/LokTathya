# Phase 7 Content Versioning Design

This document details semantic document change detection.

---

## 1. Hash Check Strategy
- **Byte hash**: SHA256 of raw data verifies exact content equivalence.
- **Semantic hash**: Stripped HTML text structures allow ignoring advertising tokens or dynamic timestamp changes.
- **Historic retention**: Re-uploaded or updated files generate a new version number increment in `src_content_version` without deleting past entries.
