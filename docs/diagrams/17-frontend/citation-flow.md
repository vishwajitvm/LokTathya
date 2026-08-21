# Citation Flow
```mermaid
graph TD
    API[FastAPI] --> DTO[CitationDTO JSON]
    DTO --> Component[<Citation /> React Component]
    Component --> DOM[Rendered Official URL + Source Name]
```
