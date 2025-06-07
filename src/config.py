# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# General configuration
DATA_SOURCE = os.getenv("DATA_SOURCE", "data/sample.csv")
EXPORT_PATH = os.getenv("EXPORT_PATH", "data/cleaned_data.csv")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# src/extract.py
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

# src/transform.py
def clean_data(df):
    # Example transformation: drop nulls and sort by date
    df_clean = df.dropna()
    if 'date' in df_clean.columns:
        df_clean = df_clean.sort_values(by='date')
    print("Data cleaned and sorted")
    return df_clean

# src/model.py
def analyze_trends(df):
    # Placeholder trend analysis logic
    trend_summary = df.describe()  # Example: summary statistics
    print("Trend analysis complete")
    return trend_summary

# src/summarize.py
def generate_summary(df):
    # Placeholder for Gemini API integration
    print("Generating summary with Gemini 1.5...")
    return "This is a placeholder summary."

# src/export.py
def export_to_csv(df, path):
    df.to_csv(path, index=False)
    print(f"Data exported to {path}")
