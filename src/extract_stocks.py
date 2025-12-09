import logging
import time
import yfinance as yf
import pandas as pd
from opentelemetry import trace

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

def fetch_stock_data_yf(symbol, period="6mo", interval="1d", max_retries=5, backoff=3):
    with tracer.start_as_current_span(
        "fetch_stock_data",
        attributes={"symbol": symbol, "period": period, "interval": interval},
    ):
        for attempt in range(1, max_retries + 1):
            df = yf.download(symbol, period=period, interval=interval)

            # Flatten MultiIndex columns if they exist
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [col[0] for col in df.columns]

            if not df.empty:
                df.reset_index(inplace=True)
                df.rename(columns={"Date": "date", "Adj Close": "adjusted_close"}, inplace=True)
                df["Ticker"] = symbol
                logger.info("Fetched %s rows for %s using yfinance", len(df), symbol)
                return df
            else:
                logger.warning(
                    "Attempt %s: No data fetched for %s. Retrying in %s seconds...",
                    attempt,
                    symbol,
                    backoff,
                )
                time.sleep(backoff)
                backoff *= 2  # Exponential backoff

    raise ValueError(f"Failed to fetch data for {symbol} after {max_retries} attempts.")
