import pytest
from datetime import datetime, timezone
from services.normalization import NormalizationService

def test_normalize_numeric():
    assert NormalizationService.normalize_numeric("₹1,25,000") == 125000.0
    assert NormalizationService.normalize_numeric("1.25 lakh") == 125000.0
    assert NormalizationService.normalize_numeric("2.5 crore") == 25000000.0
    assert NormalizationService.normalize_numeric("12.5%") == 0.125
    assert NormalizationService.normalize_numeric("(4,500)") == -4500.0

def test_normalize_date():
    assert NormalizationService.normalize_date("2024-04-01") == datetime(2024, 4, 1, tzinfo=timezone.utc)
    assert NormalizationService.normalize_date("01-04-2024") == datetime(2024, 4, 1, tzinfo=timezone.utc)

def test_normalize_period():
    res = NormalizationService.normalize_period("2024-25")
    assert res["period_type"] == "FINANCIAL_YEAR"
    assert res["period_start"] == datetime(2024, 4, 1, tzinfo=timezone.utc)
    assert res["period_end"] == datetime(2025, 3, 31, 23, 59, 59, tzinfo=timezone.utc)

    res_cal = NormalizationService.normalize_period("2026")
    assert res_cal["period_type"] == "CALENDAR_YEAR"
    assert res_cal["period_start"] == datetime(2026, 1, 1, tzinfo=timezone.utc)
