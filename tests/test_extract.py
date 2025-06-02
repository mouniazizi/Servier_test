import pandas as pd
from src.extract.extract_files import extract_csv, extract_json_with_fix
from pathlib import Path

def test_extract_csv(tmp_path):
    test_file = tmp_path / "test.csv"
    test_file.write_text("col1,col2\n1,2\n3,4")
    df = extract_csv(test_file)
    assert df.shape == (2, 2)
    assert list(df.columns) == ["col1", "col2"]

def test_extract_json_with_fix(tmp_path):
    test_file = tmp_path / "test.json"
    test_file.write_text('[{"a": 1}, {"a": 2},]')
    df = extract_json_with_fix(test_file)
    assert df.shape == (2, 1)
    assert "a" in df.columns
