import logging
import uuid

import pandas as pd
from opentelemetry import trace

from src.config import get_settings, get_top_performing_stocks
from src.export import export_to_csv
from src.extract_stocks import fetch_stock_data_yf
from src.model import analyze_trends
from src.observability import setup_logging, setup_metrics, setup_tracing
from src.summarize import generate_summary
from src.transform import clean_data
from src.upload import upload_to_bigquery

logger = logging.getLogger(__name__)


def main():
    settings = get_settings()
    setup_logging(settings.log_level)
    tracer = setup_tracing()
    meter = setup_metrics()

    run_id = str(uuid.uuid4())
    run_counter = meter.create_counter("trendnest.pipeline.runs", description="Number of pipeline runs")
    ticker_counter = meter.create_counter("trendnest.pipeline.tickers_processed", description="Tickers processed")
    row_counter = meter.create_counter("trendnest.pipeline.rows_processed", description="Rows processed")

    logger.info("Starting TrendNest pipeline", extra={"run_id": run_id})

    tickers = get_top_performing_stocks()
    logger.info("Tickers to process: %s", ", ".join(tickers), extra={"run_id": run_id})

    combined_df = []

    with tracer.start_as_current_span("pipeline", attributes={"run.id": run_id, "tickers.count": len(tickers)}):
        run_counter.add(1, attributes={"environment": settings.environment})

        for symbol in tickers:
            with tracer.start_as_current_span(
                "process_ticker",
                attributes={"ticker": symbol, "run.id": run_id},
            ):
                logger.info("Fetching live stock data for %s", symbol, extra={"run_id": run_id})
                df_raw = fetch_stock_data_yf(symbol)
                if df_raw is None or df_raw.empty:
                    logger.warning("No data for %s. Skipping.", symbol, extra={"run_id": run_id})
                    continue

                logger.info("Fetched %s rows for %s", len(df_raw), symbol, extra={"run_id": run_id})

                # Transform
                df_clean = clean_data(df_raw)
                df_clean["Ticker"] = symbol

                # Analyze
                trend_output = analyze_trends(df_clean)

                # Summarize
                summary = generate_summary(trend_output)
                logger.info("AI Summary (%s): %s", symbol, summary, extra={"run_id": run_id})

                logger.debug("Columns for %s: %s", symbol, df_clean.columns.tolist(), extra={"run_id": run_id})
                combined_df.append(df_clean)
                ticker_counter.add(1, attributes={"ticker": symbol, "environment": settings.environment})

        if combined_df:
            full_df = pd.concat(combined_df, ignore_index=True)
            row_counter.add(len(full_df), attributes={"environment": settings.environment})
            export_to_csv(full_df, settings.export_path)
            upload_to_bigquery(full_df)

    logger.info("Pipeline complete", extra={"run_id": run_id})


if __name__ == "__main__":
    main()
