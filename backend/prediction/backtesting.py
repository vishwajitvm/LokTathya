from typing import Dict, Any, List

class BacktestingEngine:
    """Strict temporal evaluation engine preventing data leakage."""
    
    @staticmethod
    def generate_temporal_splits(election_years: List[int]) -> List[Dict[str, List[int]]]:
        """
        NEVER use random train/test splitting. 
        Forces expanding historical windows (e.g. Train <= 2014, Predict 2019).
        """
        sorted_years = sorted(election_years)
        splits = []
        for i in range(1, len(sorted_years)):
            train_years = sorted_years[:i]
            predict_year = sorted_years[i]
            splits.append({
                "train_cutoff": train_years[-1],
                "train": train_years,
                "predict": [predict_year]
            })
        return splits
