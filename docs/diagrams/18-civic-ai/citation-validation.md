# Citation Validation
```mermaid
graph TD
    LLM[Draft Output] --> Check{Numbers in draft match evidence?}
    Check -->|No| Strip[Strip Block / Regenerate]
    Check -->|Yes| OK[Pass to Frontend with Source]
```
