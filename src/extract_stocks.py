import yfinance as yf
import pandas as pd

def fetch_stock_data_yf(symbol: str, period="6mo", interval="1d") -> pd.DataFrame:
    df = yf.download(symbol, period=period, interval=interval, auto_adjust=True)
    df = df[["Close", "Volume"]].rename(columns={"Close": "adjusted_close", "Volume": "volume"})
    df = df.reset_index().rename(columns={"Date": "date"})
    print(f"Fetched {len(df)} rows for {symbol} using yfinance")
    return df