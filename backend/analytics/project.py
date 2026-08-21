from typing import Dict

class ProjectAnalytics:
    @staticmethod
    def calculate_project_status_rates(total: int, completed: int, in_progress: int, on_hold: int) -> Dict[str, float]:
        if total == 0:
            return {"completion_rate": 0.0, "status": "INSUFFICIENT_DATA"}
        return {
            "completion_rate": completed / total,
            "in_progress_rate": in_progress / total,
            "on_hold_rate": on_hold / total,
            "status": "COMPLETE"
        }
