# Phase 7 Format Processing Factory

This document outlines structural parsers and file safety logic.

---

## 1. Magic Bytes Validation
- Never trusts filename extensions alone. Checks magic numbers to verify files like zip archives, XML, and PDFs before parsing.
- Safe parsers defuse XML XXE and DOCTYPE entities immediately.
- Zip member bounds checks protect against Zip Slip.
