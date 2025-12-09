import os
import pytest
from dotenv import load_dotenv

# Explicitly load .env from the project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

from src.extract_stocks import fetch_stock_data_yf


@pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="Integration test skipped by default; set RUN_INTEGRATION_TESTS=1 to run.",
)
def test_fetch_yfinance_integration():
    df = fetch_stock_data_yf("AAPL")
    assert df is not None
    # Basic shape expectations
    assert "date" in df.columns
    assert len(df) > 0
