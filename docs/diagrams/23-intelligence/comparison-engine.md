# Comparison Engine
```mermaid
graph TD
    User[Comparison Request] --> API[/api/v1/intelligence/compare]
    API --> Check{Data Origin Valid?}
    Check -->|Synthetic| Reject[Reject or Flag as Test]
    Check -->|Official| Math[Deterministic Math]
    Math --> Conflict{Phase 9A Conflicts?}
    Conflict -->|Yes| Flag[Emit CONFLICTED DATA]
    Conflict -->|No| Compare[Generate Factual Output]
    Compare --> UI[Frontend Table]
```
