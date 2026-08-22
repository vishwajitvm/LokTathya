# API EDGE CASE MATRIX

## SOURCE EDGE CASES
| SCENARIO | EXPECTED_BEHAVIOR | IMPLEMENTATION | TEST | STATUS |
|---|---|---|---|---|
| source disappears | Return 404 from source, preserve history | `FetchEvent` status code 404 | None | STUB |
| domain changes | Record redirect and new domain | `FetchEvent` redirect tracking | None | STUB |
| 500 server error | Record fetch failure, do not retry endlessly | `FetchEvent` error_message | None | STUB |
| rate limit | Backoff and quarantine | Circuit breaker | None | MISSING |

## DOCUMENT EDGE CASES
| SCENARIO | EXPECTED_BEHAVIOR | IMPLEMENTATION | TEST | STATUS |
|---|---|---|---|---|
| same URL, same content | FetchEvent recorded, no new ContentVersion | `pdf_processor.py` | `test_versioning.py` | IMPLEMENTED |
| same URL, changed content | FetchEvent recorded, new ContentVersion | `pdf_processor.py` | `test_versioning.py` | IMPLEMENTED |
| identical hash | Map to same ContentVersion | `pdf_processor.py` | `test_versioning.py` | IMPLEMENTED |
| OCR failure | Quarantine document | Quarantine logic | None | MISSING |

## DATASET EDGE CASES
| SCENARIO | EXPECTED_BEHAVIOR | IMPLEMENTATION | TEST | STATUS |
|---|---|---|---|---|
| duplicate rows | Filter or explicitly flag | TBD | None | MISSING |
| changed schema | Flag for manual mapping | TBD | None | MISSING |

## ENTITY RESOLUTION EDGE CASES
| SCENARIO | EXPECTED_BEHAVIOR | IMPLEMENTATION | TEST | STATUS |
|---|---|---|---|---|
| spelling variation | Fuzzy match, explicit confirmation | `entity_resolution.py` | None | STUB |
| duplicate names | Do not auto-merge | `sys_entity_resolution` table | None | STUB |

## GEOGRAPHY EDGE CASES
| SCENARIO | EXPECTED_BEHAVIOR | IMPLEMENTATION | TEST | STATUS |
|---|---|---|---|---|
| district renamed | Use valid_from/valid_until | `models/geography.py` | None | MISSING |
| boundary changed | Create new geometry, relate to old | `geo_relationship` | None | MISSING |
