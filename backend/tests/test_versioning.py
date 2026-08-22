import pytest
from ingestion.diff_engine import DocumentDiffEngine

def test_document_diff_engine():
    engine = DocumentDiffEngine()
    
    text_a = "The budget for 2026 is 10 crore."
    text_b = "The budget for 2026 is 12 crore."
    
    res = engine.diff_text(text_a, text_b)
    assert res["status"] == "MODIFIED"
    assert res["similarity_ratio"] < 1.0
    
    tables_a = [{"row1": "val1"}]
    tables_b = [{"row1": "val1"}, {"row2": "val2"}]
    
    tab_res = engine.diff_tables(tables_a, tables_b)
    assert tab_res["status"] == "MODIFIED"
    assert len(tab_res["added"]) == 1

def test_identical_documents():
    engine = DocumentDiffEngine()
    
    text_a = "The budget for 2026 is 10 crore."
    
    res = engine.diff_text(text_a, text_a)
    assert res["status"] == "UNCHANGED"
    assert res["similarity_ratio"] == 1.0
