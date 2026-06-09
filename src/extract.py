import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

def extract_csv(filepath):
    df = pd.read_csv(filepath)
    logger.info(f"Extracted {len(df)} rows from {filepath}")
    return df