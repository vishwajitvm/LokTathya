# Quarantine Flow
```mermaid
graph TD
    Data --> Validator{Passes constraints?}
    Validator -->|Yes| NextStage
    Validator -->|No| QuarDB[(Quarantine DB)]
    QuarDB --> HumanReview
```
