import pandas as pd
from src.config import DATA_SOURCE

def extract_data():
    try:
        df = pd.read_csv(DATA_SOURCE)
        print(f"Data extracted from {DATA_SOURCE}")
        return df
    except Exception as e:
        print(f"Error extracting data: {e}")
        return pd.DataFrame()
    