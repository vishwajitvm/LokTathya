# DATA EDGE CASE MATRIX

## QUALITY EDGE CASES
| SCENARIO | EXPECTED BEHAVIOR | REQUIRED FIX | STATUS |
|----------|-------------------|--------------|--------|
| Division by zero | INSUFFICIENT_DATA | Analytics safety checks | MISSING |
| Null finance vals | Record as None, do not default 0 | Validation rules | MISSING |
| Conflicting units| Quarantine or track explicitly | Unit normalization pipeline | MISSING |

## RESOLUTION EDGE CASES
| SCENARIO | EXPECTED BEHAVIOR | REQUIRED FIX | STATUS |
|----------|-------------------|--------------|--------|
| Duplicate names | AMBIGUOUS state | EntityResolution service | MISSING |
| Schema change | Quarantine dataset | Schema fingerprinting | MISSING |
| Date parsing | Preserve raw, extract normalized | DateNormalizer | MISSING |
