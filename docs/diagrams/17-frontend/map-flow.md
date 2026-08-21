# Map Flow
```mermaid
graph TD
    GeogAPI[/api/v1/geographies/id] --> GeoJSON[Simplified GeoJSON Response]
    GeoJSON --> MapComp[<MapContainer /> client-side]
    MapComp --> Render[Interactive Canvas]
```
