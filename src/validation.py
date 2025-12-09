import logging
from typing import Iterable, List

import pandas as pd
from opentelemetry import trace

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

REQUIRED_COLUMNS = ("date", "Close", "Volume")


def validate_schema(df: pd.DataFrame) -> List[str]:
    """
    Validate that required columns exist and contain non-empty data.
    Returns a list of error messages (empty if valid).
    """
    errors: List[str] = []
    with tracer.start_as_current_span("validate_schema"):
        for col in REQUIRED_COLUMNS:
            if col not in df.columns:
                errors.append(f"Missing required column: {col}")
        if df.empty:
            errors.append("DataFrame is empty")
        if "Volume" in df.columns and (df["Volume"] <= 0).all():
            errors.append("Volume column has no positive values")
        if "Close" in df.columns and (df["Close"] <= 0).all():
            errors.append("Close column has no positive values")

        if errors:
            logger.warning("Validation errors: %s", errors)
        return errors
