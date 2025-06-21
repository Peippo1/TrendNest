# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# General configuration
DATA_SOURCE = os.getenv("DATA_SOURCE", "data/sample.csv")
EXPORT_PATH = os.getenv("EXPORT_PATH", "data/cleaned_data.csv")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Fetch top performing stocks (e.g. based on % daily change)
def get_top_performing_stocks(limit=10):
    import yfinance as yf

    # Example stock universe (expandable)
    symbols = [
        "AAPL", "MSFT", "GOOGL", "NVDA", "AMZN", "TSLA", "META", "NFLX", "INTC", "CSCO",
        "IBM", "ADBE", "PYPL", "CRM", "ORCL"
    ]

    changes = []
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="2d")  # fetch previous and current close
        if len(hist) >= 2:
            prev_close = hist['Close'].iloc[-2]
            today_close = hist['Close'].iloc[-1]
            pct_change = ((today_close - prev_close) / prev_close) * 100
            changes.append((symbol, pct_change))

    sorted_changes = sorted(changes, key=lambda x: x[1], reverse=True)
    top_symbols = [sym for sym, _ in sorted_changes[:limit]]
    print(f"📈 Top {limit} performing stocks: {top_symbols}")
    return top_symbols
