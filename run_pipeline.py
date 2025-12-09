import logging
from opentelemetry import trace

from src.extract_stocks import fetch_stock_data_yf
from src.transform import clean_data
from src.model import analyze_trends
from src.summarize import generate_summary
from src.export import export_to_csv
from src.config import EXPORT_PATH, get_top_performing_stocks
from src.upload import upload_to_bigquery
from src.observability import setup_logging, setup_tracing
import pandas as pd

logger = logging.getLogger(__name__)


def main():
    setup_logging()
    tracer = setup_tracing()

    logger.info("Starting TrendNest pipeline")

    tickers = get_top_performing_stocks()
    logger.info("Tickers to process: %s", ", ".join(tickers))

    combined_df = []

    with tracer.start_as_current_span("pipeline") as pipeline_span:
        pipeline_span.set_attribute("tickers.count", len(tickers))

        for symbol in tickers:
            with tracer.start_as_current_span("process_ticker", attributes={"ticker": symbol}):
                logger.info("Fetching live stock data for %s", symbol)
                df_raw = fetch_stock_data_yf(symbol)
                if df_raw is None or df_raw.empty:
                    logger.warning("No data for %s. Skipping.", symbol)
                    continue

                logger.info("Fetched %s rows for %s", len(df_raw), symbol)

                # Transform
                df_clean = clean_data(df_raw)
                df_clean["Ticker"] = symbol

                # Analyze
                trend_output = analyze_trends(df_clean)

                # Summarize
                summary = generate_summary(trend_output)
                logger.info("AI Summary (%s): %s", symbol, summary)

                logger.debug("Columns for %s: %s", symbol, df_clean.columns.tolist())
                combined_df.append(df_clean)

        if combined_df:
            full_df = pd.concat(combined_df, ignore_index=True)
            export_to_csv(full_df, EXPORT_PATH)
            upload_to_bigquery(full_df)

    logger.info("Pipeline complete")

if __name__ == "__main__":
    main()
