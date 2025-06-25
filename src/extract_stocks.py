import time
import yfinance as yf
import pandas as pd

def fetch_stock_data_yf(symbol, period="6mo", interval="1d", max_retries=5, backoff=3):
    for attempt in range(1, max_retries + 1):
        df = yf.download(symbol, period=period, interval=interval)

        # Flatten MultiIndex columns if they exist
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0] for col in df.columns]

        if not df.empty:
            df.reset_index(inplace=True)
            df.rename(columns={"Date": "date", "Adj Close": "adjusted_close"}, inplace=True)
            df["Ticker"] = symbol
            print(f"Fetched {len(df)} rows for {symbol} using yfinance")
            return df
        else:
            print(f"⚠️ Attempt {attempt}: No data fetched for {symbol}. Retrying in {backoff} seconds...")
            time.sleep(backoff)
            backoff *= 2  # Exponential backoff

    raise ValueError(f"❌ Failed to fetch data for {symbol} after {max_retries} attempts.")
