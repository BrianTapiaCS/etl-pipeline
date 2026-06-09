import pandas as pd
import pytest
from src.extract import extract_csv

def test_extract_csv_returns_dataframe():
    df = extract_csv('data/customers.csv')
    assert isinstance(df, pd.DataFrame)

def test_extract_csv_has_correct_columns():
    df = extract_csv('data/customers.csv')
    assert 'customer_id' in df.columns
    assert 'first_name' in df.columns
    assert 'email' in df.columns

def test_extract_csv_row_count():
    df = extract_csv('data/customers.csv')
    assert len(df) == 6