from typing import Dict, Optional

class FinancialAnalytics:
    @staticmethod
    def calculate_utilization_rate(allocated: float, expenditure: float) -> Dict[str, Optional[float]]:
        if allocated is None or allocated == 0:
            return {"rate": None, "status": "INSUFFICIENT_DATA"}
        return {"rate": expenditure / allocated, "status": "COMPLETE"}

    @staticmethod
    def calculate_unreconciled_amount(allocated: float, released: float, expenditure: float) -> Dict[str, Optional[float]]:
        unspent_released = released - expenditure
        return {"unspent_released": unspent_released, "unreleased_allocation": allocated - released}
