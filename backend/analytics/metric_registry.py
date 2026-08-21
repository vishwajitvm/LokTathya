from typing import Dict, Any

class MetricRegistry:
    def __init__(self):
        self.metrics = {}

    def register(self, metric_id: str, name: str, formula: str, version: str):
        self.metrics[metric_id] = {
            "metric_id": metric_id,
            "name": name,
            "formula": formula,
            "version": version,
            "status": "ACTIVE"
        }

registry = MetricRegistry()
registry.register("METRIC-FIN-UTILIZATION-001", "Utilization Rate", "expenditure / allocated", "1.0")
registry.register("METRIC-FIN-RELEASE-RATE-001", "Release Rate", "released / allocated", "1.0")
