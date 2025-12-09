import argparse
import logging
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

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
from src.validation import validate_schema

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Run TrendNest pipeline.")
    parser.add_argument("--tickers", help="Comma-separated tickers to process (override selection).")
    parser.add_argument("--limit", type=int, help="Limit top performers selection.")
    parser.add_argument("--export-path", help="Override export path for cleaned data.")
    parser.add_argument("--dead-letter-path", help="Override path for failed rows CSV.")
    return parser.parse_args()


def main():
    settings = get_settings()
    setup_logging(settings.log_level)
    tracer = setup_tracing()
    meter = setup_metrics()

    run_id = str(uuid.uuid4())
    run_counter = meter.create_counter("trendnest.pipeline.runs", description="Number of pipeline runs")
    ticker_counter = meter.create_counter("trendnest.pipeline.tickers_processed", description="Tickers processed")
    row_counter = meter.create_counter("trendnest.pipeline.rows_processed", description="Rows processed")
    retry_counter = meter.create_counter("trendnest.pipeline.fetch_retries", description="Fetch retries")
    failure_counter = meter.create_counter("trendnest.pipeline.failures", description="Per-ticker failures")

    logger.info("Starting TrendNest pipeline", extra={"run_id": run_id})

    args = parse_args()

    if args.tickers:
        tickers = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]
    else:
        tickers = get_top_performing_stocks(limit=args.limit)

    export_path = args.export_path or settings.export_path
    dead_letter_path = args.dead_letter_path or settings.dead_letter_path

    logger.info("Tickers to process: %s", ", ".join(tickers), extra={"run_id": run_id})

    combined_df = []
    failed_rows = []

    with tracer.start_as_current_span("pipeline", attributes={"run.id": run_id, "tickers.count": len(tickers)}):
        run_counter.add(1, attributes={"environment": settings.environment})

        with ThreadPoolExecutor(max_workers=settings.max_workers) as executor:
            future_map = {
                executor.submit(process_ticker, tracer, ticker, run_id, ticker_counter, retry_counter, settings): ticker
                for ticker in tickers
            }
            for future in as_completed(future_map):
                symbol = future_map[future]
                try:
                    result = future.result()
                    if result is None:
                        continue
                    df_clean, summary = result
                    combined_df.append(df_clean)
                    logger.info("AI Summary (%s): %s", symbol, summary, extra={"run_id": run_id})
                except Exception as e:
                    logger.exception("Failed processing %s: %s", symbol, e, extra={"run_id": run_id})
                    failed_rows.append({"Ticker": symbol, "error": str(e)})
                    failure_counter.add(1, attributes={"ticker": symbol, "environment": settings.environment})

        if combined_df:
            full_df = pd.concat(combined_df, ignore_index=True)
            row_counter.add(len(full_df), attributes={"environment": settings.environment})
            export_to_csv(full_df, export_path)
            upload_to_bigquery(full_df)

        if failed_rows:
            pd.DataFrame(failed_rows).to_csv(dead_letter_path, index=False)
            logger.warning("Failed rows written to %s", dead_letter_path, extra={"run_id": run_id})

    logger.info("Pipeline complete", extra={"run_id": run_id})


def process_ticker(tracer, symbol, run_id, ticker_counter, retry_counter, settings):
    with tracer.start_as_current_span(
        "process_ticker",
        attributes={"ticker": symbol, "run.id": run_id},
    ):
        logger.info("Fetching live stock data for %s", symbol, extra={"run_id": run_id})
        df_raw, attempts = fetch_stock_data_yf(
            symbol,
            max_retries=settings.fetch_retries,
            backoff=settings.fetch_backoff,
            timeout=settings.fetch_timeout,
        )
        if df_raw is None or df_raw.empty:
            logger.warning("No data for %s. Skipping.", symbol, extra={"run_id": run_id})
            return None

        logger.info("Fetched %s rows for %s", len(df_raw), symbol, extra={"run_id": run_id})

        # Transform
        df_clean = clean_data(df_raw)
        df_clean["Ticker"] = symbol

        errors = validate_schema(df_clean)
        if errors:
            raise ValueError(f"Schema validation failed for {symbol}: {errors}")

        # Analyze
        trend_output = analyze_trends(df_clean)

        # Summarize
        summary = generate_summary(trend_output)

        logger.debug("Columns for %s: %s", symbol, df_clean.columns.tolist(), extra={"run_id": run_id})
        ticker_counter.add(1, attributes={"ticker": symbol, "environment": settings.environment})
        if attempts > 1:
            retry_counter.add(attempts - 1, attributes={"ticker": symbol, "environment": settings.environment})
        return df_clean, summary


if __name__ == "__main__":
    main()
