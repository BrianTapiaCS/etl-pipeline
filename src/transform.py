import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

def transform(df):
    logger.info(f"Before cleaning: {len(df)} rows")
    
    rejects = []

    # check for missing values
    missing = df[df.isnull().any(axis=1)]
    for _, row in missing.iterrows():
        rejects.append({'row': row.to_dict(), 'reason': 'missing value'})
    df = df.dropna()

    # check for invalid emails
    invalid_email = df[~df['email'].str.contains('@')]
    for _, row in invalid_email.iterrows():
        rejects.append({'row': row.to_dict(), 'reason': 'invalid email'})
    df = df[df['email'].str.contains('@')]

    # check for duplicates
    dupes = df[df.duplicated(subset=['customer_id'])]
    for _, row in dupes.iterrows():
        rejects.append({'row': row.to_dict(), 'reason': 'duplicate customer_id'})
    df = df.drop_duplicates(subset=['customer_id'])

    logger.info(f"After cleaning: {len(df)} rows | Rejected: {len(rejects)} rows")
    return df, rejects