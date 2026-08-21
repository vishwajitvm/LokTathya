# Source Deprecation
```mermaid
graph TD
    Ping[Health Check] --> Detect{Status?}
    Detect -->|200 OK| Active[ACTIVE]
    Detect -->|503 Temp| Temp[TEMPORARILY_UNAVAILABLE]
    Detect -->|404 Permanent| Dep[DEPRECATED]
    Temp -.-> Ping
    Dep --> Freeze[Freeze Historical Data]
```
