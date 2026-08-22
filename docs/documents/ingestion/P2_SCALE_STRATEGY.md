# P2 Scale Strategy

## Purpose
Provides scaling guidelines for processing millions of civic records.

## Scaling Architecture Diagram
Refer to [scaling-architecture.mmd](file:///c:/python/LokTathya/docs/diagrams/10-scaling/scaling-architecture.mmd) for independent worker layouts.

## Key Strategies
1. **Streaming Processing**: Ensure heavy XLSX files are processed in chunked memory generators instead of raw RAM reads.
2. **Queue Separation**: Bounded queue concurrency prevents heavy PDF/OCR tasks from blocking lightweight HTML discovery runs.
