"""Tests for data ingestion functions."""

import pytest
import pandas as pd
from data_processing.ingestion import load_csv, load_json, load_excel

def test_load_csv_success():
    """Test loading real CSV file."""
    df = load_csv('data/circulation_data.csv')

    assert len(df) > 0
    assert 'transaction_id' in df.columns

def test_load_csv_file_not_found():
    """Test error handling when file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        load_csv('data/nonexistent.csv')

def test_load_json_success():
    """Test loading real JSON file."""
    df = load_json('data/events_data.json')

    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)

# Add more tests using tmp_path to create test files on the fly:

def test_load_csv_empty_file(tmp_path):
    """Test that an empty CSV raises an error."""
    empty = tmp_path / "empty.csv"
    empty.write_text("")
    with pytest.raises(pd.errors.EmptyDataError):
        load_csv(str(empty))

def test_load_json_file_not_found():
    """Test error handling when JSON file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        load_json('data/nonexistent.json')

def test_load_json_invalid(tmp_path):
    """Test that invalid JSON raises an error."""
    import json
    bad = tmp_path / "bad.json"
    bad.write_text("not valid json {{{")
    with pytest.raises(json.JSONDecodeError):
        load_json(str(bad))

def test_load_excel_file_not_found(tmp_path):
    fake_path = tmp_path / "missing.xlsx"
    with pytest.raises(FileNotFoundError):
        load_excel(fake_path)


def test_load_excel_invalid_content(tmp_path):
    bad_excel = tmp_path / "bad.xlsx"
    bad_excel.write_text("not an excel file")

def test_load_excel_empty_sheet(tmp_path):
    excel_file = tmp_path / "empty.xlsx"

    pd.DataFrame().to_excel(
        excel_file,
        index=False
    )

    result = load_excel(str(excel_file))

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0