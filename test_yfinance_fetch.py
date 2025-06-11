from dotenv import load_dotenv
import os

# Explicitly load .env from the project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

from src.extract_stocks import fetch_stock_data_yf

df = fetch_stock_data_yf("AAPL")
print(df.head())