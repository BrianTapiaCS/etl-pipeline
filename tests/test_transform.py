import pandas as pd
from src.transform import transform

def test_removes_missing_values():
    data = {'customer_id': [1, 2], 'first_name': ['John', 'Bob'], 'last_name': ['Doe', None], 'email': ['john@example.com', 'bob@example.com'], 'created_at': ['2024-01-01', '2024-01-02']}
    df = pd.DataFrame(data)
    clean_df, rejects = transform(df)
    assert len(clean_df) == 1
    assert len(rejects) == 1
    assert rejects[0]['reason'] == 'missing value'

def test_removes_invalid_emails():
    data = {'customer_id': [1, 2], 'first_name': ['John', 'Alice'], 'last_name': ['Doe', 'Johnson'], 'email': ['john@example.com', 'alicejohnson.com'], 'created_at': ['2024-01-01', '2024-01-02']}
    df = pd.DataFrame(data)
    clean_df, rejects = transform(df)
    assert len(clean_df) == 1
    assert rejects[0]['reason'] == 'invalid email'

def test_removes_duplicates():
    data = {'customer_id': [1, 1], 'first_name': ['John', 'John'], 'last_name': ['Doe', 'Doe'], 'email': ['john@example.com', 'john@example.com'], 'created_at': ['2024-01-01', '2024-01-01']}
    df = pd.DataFrame(data)
    clean_df, rejects = transform(df)
    assert len(clean_df) == 1
    assert rejects[0]['reason'] == 'duplicate customer_id'

def test_clean_data_passes_through():
    data = {'customer_id': [1, 2], 'first_name': ['John', 'Jane'], 'last_name': ['Doe', 'Smith'], 'email': ['john@example.com', 'jane@example.com'], 'created_at': ['2024-01-01', '2024-01-02']}
    df = pd.DataFrame(data)
    clean_df, rejects = transform(df)
    assert len(clean_df) == 2
    assert len(rejects) == 0