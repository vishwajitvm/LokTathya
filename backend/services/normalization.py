import re
from datetime import datetime, timezone
from typing import Dict, Any, Optional

class NormalizationService:
    """
    Step 3: Type Normalization Engine.
    Handles Rupees, lakh, crore, percentages, negative accounts, dates, and periods.
    """

    @staticmethod
    def normalize_numeric(raw_val: str) -> Optional[float]:
        if not raw_val:
            return None
            
        cleaned = raw_val.strip().replace(" ", "").replace(",", "")
        
        # Indian Currency Symbol removal
        cleaned = cleaned.replace("₹", "").replace("Rs.", "").replace("Rs", "")
        
        # Check negative accounting value wrapped in parentheses: (4,500) -> -4500
        is_negative = False
        if cleaned.startswith("(") and cleaned.endswith(")"):
            is_negative = True
            cleaned = cleaned[1:-1]

        # Check percentage: 12.5% -> 0.125
        is_percentage = False
        if cleaned.endswith("%"):
            is_percentage = True
            cleaned = cleaned[:-1]

        # Indian Numbering multipliers
        multiplier = 1.0
        lower_val = cleaned.lower()
        if "lakh" in lower_val:
            multiplier = 100000.0
            cleaned = re.sub(r'lakhs?', '', lower_val)
        elif "crore" in lower_val:
            multiplier = 10000000.0
            cleaned = re.sub(r'crores?', '', lower_val)
            
        try:
            val = float(cleaned) * multiplier
            if is_percentage:
                val = val / 100.0
            if is_negative:
                val = -val
            return val
        except ValueError:
            return None

    @staticmethod
    def normalize_date(raw_val: str) -> Optional[datetime]:
        if not raw_val:
            return None
            
        # Clean whitespace and standard formats
        cleaned = raw_val.strip()
        
        for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
            try:
                # Parse to offset-aware UTC
                dt = datetime.strptime(cleaned, fmt)
                return dt.replace(tzinfo=timezone.utc)
            except ValueError:
                continue
        return None

    @staticmethod
    def normalize_period(raw_val: str) -> Dict[str, Any]:
        """
        Extract financial year (e.g. 2024-25), election year, or date ranges.
        """
        cleaned = raw_val.strip()
        
        # Financial year check: e.g. 2024-25 or 2024-2025
        fy_match = re.match(r'^(\d{4})[-/](\d{2,4})$', cleaned)
        if fy_match:
            start_year = int(fy_match.group(1))
            end_group = fy_match.group(2)
            
            if len(end_group) == 2:
                # 25 -> 2025
                century = start_year // 100
                end_year = century * 100 + int(end_group)
            else:
                end_year = int(end_group)
                
            return {
                "period_type": "FINANCIAL_YEAR",
                "period_start": datetime(start_year, 4, 1, tzinfo=timezone.utc),
                "period_end": datetime(end_year, 3, 31, 23, 59, 59, tzinfo=timezone.utc),
                "original_period": raw_val
            }
            
        # Single Year check (e.g. 2024)
        year_match = re.match(r'^(\d{4})$', cleaned)
        if year_match:
            year = int(year_match.group(1))
            return {
                "period_type": "CALENDAR_YEAR",
                "period_start": datetime(year, 1, 1, tzinfo=timezone.utc),
                "period_end": datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc),
                "original_period": raw_val
            }

        return {
            "period_type": "UNKNOWN",
            "period_start": None,
            "period_end": None,
            "original_period": raw_val
        }
