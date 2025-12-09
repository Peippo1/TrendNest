# src/config.py
import logging
from functools import lru_cache
from typing import List

from dotenv import load_dotenv
from opentelemetry import trace
from pydantic import BaseSettings, Field, validator

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

load_dotenv()


class Settings(BaseSettings):
    # General configuration
    data_source: str = Field("data/sample.csv", env="DATA_SOURCE")
    export_path: str = Field("data/cleaned_data.csv", env="EXPORT_PATH")
    dead_letter_path: str = Field("data/failed_rows.csv", env="DEAD_LETTER_PATH")

    # Gemini / AI
    gemini_api_key: str = Field("", env="GEMINI_API_KEY")

    # GCP / BigQuery
    gcp_project_id: str = Field("", env="GCP_PROJECT_ID")
    bq_dataset: str = Field("trendnest", env="BQ_DATASET")
    bq_table: str = Field("cleaned_stock_data", env="BQ_TABLE")
    google_credentials_path: str = Field("", env="GOOGLE_APPLICATION_CREDENTIALS")

    # Observability
    log_level: str = Field("INFO", env="LOG_LEVEL")
    environment: str = Field("dev", env="ENVIRONMENT")
    otel_exporter_otlp_endpoint: str = Field("", env="OTEL_EXPORTER_OTLP_ENDPOINT")
    otel_exporter_otlp_headers: str = Field("", env="OTEL_EXPORTER_OTLP_HEADERS")

    # Tickers
    top_performers_limit: int = Field(10, env="TOP_PERFORMERS_LIMIT")
    tickers_universe: List[str] = Field(
        default_factory=lambda: [
            "AAPL", "MSFT", "GOOGL", "NVDA", "AMZN", "TSLA", "META", "NFLX", "INTC", "CSCO",
            "IBM", "ADBE", "PYPL", "CRM", "ORCL",
        ]
    )
    max_workers: int = Field(4, env="MAX_WORKERS")
    fetch_timeout: int = Field(15, env="FETCH_TIMEOUT_SECONDS")
    fetch_retries: int = Field(5, env="FETCH_MAX_RETRIES")
    fetch_backoff: int = Field(3, env="FETCH_BACKOFF_SECONDS")

    @validator("log_level")
    def normalize_log_level(cls, v: str) -> str:
        return v.upper()

    @validator("tickers_universe", pre=True)
    def split_tickers(cls, v):
        if isinstance(v, str):
            return [item.strip().upper() for item in v.split(",") if item.strip()]
        return v

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Fetch top performing stocks (e.g. based on % daily change)
def get_top_performing_stocks(limit: int | None = None) -> List[str]:
    import yfinance as yf

    settings = get_settings()
    selected_limit = limit or settings.top_performers_limit

    symbols = settings.tickers_universe

    changes = []
    with tracer.start_as_current_span("select_top_performers", attributes={"universe_size": len(symbols)}):
        for symbol in symbols:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")  # fetch previous and current close
            if len(hist) >= 2:
                prev_close = hist['Close'].iloc[-2]
                today_close = hist['Close'].iloc[-1]
                pct_change = ((today_close - prev_close) / prev_close) * 100
                changes.append((symbol, pct_change))

        sorted_changes = sorted(changes, key=lambda x: x[1], reverse=True)
        top_symbols = [sym for sym, _ in sorted_changes[:selected_limit]]
        logger.info("Top %s performing stocks: %s", selected_limit, top_symbols)
        return top_symbols
