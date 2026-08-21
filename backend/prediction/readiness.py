from typing import Dict, Any, List

class ForecastingReadinessEngine:
    """Evaluates whether LokTathya has sufficient data quality/depth to support forecasting."""
    
    @staticmethod
    def evaluate_readiness(election_dataset_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determines readiness strictly based on historical depth, missingness, and boundary continuity.
        """
        years_covered = election_dataset_metrics.get("years_covered", 0)
        missing_rate = election_dataset_metrics.get("missing_results_rate", 1.0)
        boundary_continuity = election_dataset_metrics.get("boundary_continuity_rate", 0.0)

        # Hard constraints for scientifically defensible prediction
        if years_covered < 10 or missing_rate > 0.15 or boundary_continuity < 0.8:
            return {
                "status": "NOT_READY",
                "reason": "Insufficient historical depth, excessive missing data, or geographic boundary instability.",
                "metrics": election_dataset_metrics
            }
            
        return {
            "status": "PARTIALLY_READY",
            "reason": "Baseline models can be evaluated, but deep spatial analysis requires further alignment.",
            "metrics": election_dataset_metrics
        }
