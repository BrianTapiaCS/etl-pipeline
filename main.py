from src.extract import extract_csv
from src.transform import transform
from src.load import load_to_postgres
from src.config import load_config

config = load_config()
source = config['sources'][0]

df = extract_csv(source['path'])
df, rejects = transform(df)
load_to_postgres(df, rejects)