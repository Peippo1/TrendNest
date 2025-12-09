import os
import pytest
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from src.upload import upload_to_bigquery


@pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="Integration test skipped by default; set RUN_INTEGRATION_TESTS=1 to run.",
)
def test_upload_integration():
    df = pd.DataFrame({"date": ["2024-01-01"], "Close": [10], "Volume": [100], "Ticker": ["AAPL"]})
    # This will raise if credentials are missing/invalid
    upload_to_bigquery(df)
