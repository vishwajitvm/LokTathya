# Phase 7A Format Audit

This document records the parser format validation audit.

---

## 1. Verified Controls
- **Mime Type Magic Bytes**: Validates Magic headers (PDF, ZIP, XML) instead of filename extensions.
- **XLSM macro check**: Avoids execution of any Excel macros.
- **XML XXE**: Rejects external DOCTYPE / ENTITY schemas immediately.
