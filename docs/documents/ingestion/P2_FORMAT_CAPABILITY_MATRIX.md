# P2 Format Capability Matrix

This matrix establishes the status of format parsers implemented inside the LokTathya processing engine.

| Format | Status | Parser Class | Streaming | Sandbox |
| :--- | :---: | :--- | :---: | :---: |
| HTML | `PASS` | `HTMLParser` | No | No |
| PDF | `PASS` | `PDFParser` | Yes | Yes |
| CSV | `PASS` | `CSVParser` | Yes | No |
| XLSX | `PASS` | `XLSXParser` | Yes | No |
| JSON | `PASS` | `JSONParser` | Yes | No |
| Shapefile | `PLANNED` | `GISParser` | No | No |

## Limitations
- OCR parsing for scanned PDFs is deferred to Phase 3.
- GeoJSON/KML GIS boundary projections will be fully implemented in a separate GIS slice.
