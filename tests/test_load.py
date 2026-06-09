import pandas as pd
from unittest.mock import patch, MagicMock
from src.load import load_to_postgres

@patch('src.load.psycopg2.connect')
def test_load_connects_to_database(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    df = pd.DataFrame({'customer_id': [1], 'first_name': ['John'], 'last_name': ['Doe'], 'email': ['john@example.com'], 'created_at': ['2024-01-01']})
    load_to_postgres(df, [])

    assert mock_connect.called

@patch('src.load.psycopg2.connect')
def test_load_inserts_clean_rows(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    df = pd.DataFrame({'customer_id': [1, 2], 'first_name': ['John', 'Jane'], 'last_name': ['Doe', 'Smith'], 'email': ['john@example.com', 'jane@example.com'], 'created_at': ['2024-01-01', '2024-01-02']})
    load_to_postgres(df, [])

    assert mock_cursor.execute.called

@patch('src.load.psycopg2.connect')
def test_load_inserts_rejects(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    df = pd.DataFrame(columns=['customer_id', 'first_name', 'last_name', 'email', 'created_at'])
    rejects = [{'row': {'customer_id': 3, 'first_name': 'Bob', 'last_name': None, 'email': 'bob@example.com', 'created_at': '2024-01-03'}, 'reason': 'missing value'}]
    load_to_postgres(df, rejects)

    assert mock_cursor.execute.called

@patch('src.load.psycopg2.connect')
def test_load_commits_transaction(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    df = pd.DataFrame(columns=['customer_id', 'first_name', 'last_name', 'email', 'created_at'])
    load_to_postgres(df, [])

    assert mock_conn.commit.called
