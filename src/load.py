import psycopg2
from dotenv import load_dotenv
import os
import json
import logging 

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

def load_to_postgres(df, rejects):
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    cursor = conn.cursor()

    # create main table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stg_customers (
            customer_id BIGINT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP
        )
    """)

    # create rejects table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stg_rejects (
            raw_payload JSONB NOT NULL,
            reason TEXT NOT NULL,
            rejected_at TIMESTAMP NOT NULL DEFAULT NOW()
        )
    """)

    # insert clean rows
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO stg_customers (customer_id, first_name, last_name, email, created_at)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (customer_id) DO NOTHING
        """, (row['customer_id'], row['first_name'], row['last_name'], row['email'], row['created_at']))

    # insert rejected rows
    for reject in rejects:
        cursor.execute("""
            INSERT INTO stg_rejects (raw_payload, reason)
            VALUES (%s, %s)
        """, (json.dumps({k: (None if str(v) == 'nan' else v) for k, v in reject['row'].items()}, default=str), reject['reason']))

    conn.commit()
    cursor.close()
    conn.close()
    logger.info(f"Loaded {len(df)} clean rows into stg_customers")
    logger.info(f"Loaded {len(rejects)} rejected rows into stg_rejects")
    logger.info("Pipeline completed successfully!")