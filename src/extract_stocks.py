import logging
import random
import time
import yfinance as yf
import pandas as pd
from opentelemetry import trace

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

DEFAULT_TIMEOUT = 15


def fetch_stock_data_yf(symbol, period="6mo", interval="1d", max_retries=5, backoff=3, timeout=DEFAULT_TIMEOUT):
    with tracer.start_as_current_span(
        "fetch_stock_data",
        attributes={"symbol": symbol, "period": period, "interval": interval},
    ):
        for attempt in range(1, max_retries + 1):
            try:
                df = yf.download(symbol, period=period, interval=interval, timeout=timeout)
            except Exception as e:
                logger.warning(
                    "Attempt %s: error fetching %s (%s). Retrying in %s seconds...",
                    attempt,
                    symbol,
                    e,
                    backoff,
                )
                time.sleep(backoff + random.random())
                backoff *= 2
                continue

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
                time.sleep(backoff + random.random())
                backoff *= 2  # Exponential backoff

    raise ValueError(f"Failed to fetch data for {symbol} after {max_retries} attempts.")
