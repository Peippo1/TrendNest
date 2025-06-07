import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

ALPHA_API_KEY = os.getenv("ALPHA_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"

def fetch_daily_stock_data(symbol: str, outputsize="compact"):
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "outputsize": outputsize,
        "apikey": ALPHA_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "Time Series (Daily)" not in data:
        raise ValueError(f"Failed to fetch data: {data.get('Error Message', 'Unknown error')}")

    ts_data = data["Time Series (Daily)"]
    df = pd.DataFrame.from_dict(ts_data, orient="index")
    df = df.rename(columns={
        "4. close": "close",
        "5. adjusted close": "adjusted_close",
        "6. volume": "volume"
    })
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df = df[["adjusted_close", "volume"]].astype(float)
    df = df.rename_axis("date").reset_index()
    print(f"Fetched {len(df)} rows for {symbol}")
    return df