import pandas as pd
import io
import json
from typing import Dict, Any, Tuple
from tracenest import logger

class SchemaInferenceEngine:
    """
    Infers tabular schema natively in Python using bounded sampling (pandas chunking)
    to prevent memory exhaustion on large civic datasets.
    """
    
    def __init__(self, sample_rows: int = 1000):
        self.sample_rows = sample_rows

    def infer_schema(self, content_bytes: bytes, format_type: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Returns:
            inferred_schema (dict)
            quality_profile (dict)
        """
        if format_type not in ["CSV", "XLSX", "TSV"]:
            return self._fallback_schema(), self._fallback_profile()
            
        try:
            if format_type == "CSV":
                # Use chunking to read only the sample_rows
                df_iter = pd.read_csv(io.BytesIO(content_bytes), chunksize=self.sample_rows)
                df = next(df_iter)
                # Count total rows roughly by reading the rest without parsing if needed, but for now we just profile the sample.
                # Actually, reading the whole file line by line to count is fast.
                row_count = sum(1 for _ in io.BytesIO(content_bytes)) - 1
            elif format_type == "TSV":
                df_iter = pd.read_csv(io.BytesIO(content_bytes), sep='\t', chunksize=self.sample_rows)
                df = next(df_iter)
                row_count = sum(1 for _ in io.BytesIO(content_bytes)) - 1
            elif format_type == "XLSX":
                # Pandas read_excel doesn't support chunksize easily, so we read nrows
                df = pd.read_excel(io.BytesIO(content_bytes), nrows=self.sample_rows)
                # Estimating row count for xlsx requires reading the whole thing or relying on metadata.
                # Since we want to protect memory, we'll just say row_count >= len(df)
                row_count = len(df) 
                
        except Exception as e:
            logger.error("Failed to parse tabular data for schema inference", error=str(e))
            return self._fallback_schema(), self._fallback_profile()
            
        return self._build_schema(df), self._build_profile(df, row_count)

    def _build_schema(self, df: pd.DataFrame) -> Dict[str, Any]:
        columns = []
        for col in df.columns:
            series = df[col]
            dtype_str = str(series.dtype)
            
            # Map pandas dtype to standard
            if "int" in dtype_str:
                semantic = "INTEGER"
            elif "float" in dtype_str:
                semantic = "FLOAT"
            elif "datetime" in dtype_str:
                semantic = "DATETIME"
            elif "bool" in dtype_str:
                semantic = "BOOLEAN"
            else:
                semantic = "STRING"
                
            col_def = {
                "name": str(col),
                "type": semantic,
                "nullable": bool(series.isnull().any()),
                "unique": bool(series.is_unique)
            }
            columns.append(col_def)
            
        return {"columns": columns}

    def _build_profile(self, df: pd.DataFrame, total_row_count: int) -> Dict[str, Any]:
        null_count = df.isnull().sum().sum()
        total_cells = df.size
        null_ratio = float(null_count / total_cells) if total_cells > 0 else 0.0
        
        dup_count = df.duplicated().sum()
        dup_ratio = float(dup_count / len(df)) if len(df) > 0 else 0.0
        
        return {
            "row_count": total_row_count,
            "column_count": len(df.columns),
            "null_ratio": round(null_ratio, 4),
            "duplicate_row_ratio": round(dup_ratio, 4)
        }

    def _fallback_schema(self) -> Dict[str, Any]:
        return {"columns": []}
        
    def _fallback_profile(self) -> Dict[str, Any]:
        return {
            "row_count": 0,
            "column_count": 0,
            "null_ratio": 0.0,
            "duplicate_row_ratio": 0.0
        }
