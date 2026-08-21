from typing import Dict, Any

class FeatureRegistry:
    def __init__(self):
        self.features = {}

    def register(self, feature_id: str, name: str, lookahead_risk: str):
        if lookahead_risk == "HIGH":
            raise ValueError(f"Feature {feature_id} rejected due to high data leakage risk.")
            
        self.features[feature_id] = {
            "feature_id": feature_id,
            "name": name,
            "lookahead_risk": lookahead_risk,
            "status": "APPROVED"
        }

registry = FeatureRegistry()
registry.register("FEAT-ELEC-001", "Historical Vote Share", "LOW")
registry.register("FEAT-ELEC-002", "Incumbency Status", "LOW")
