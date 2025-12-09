import logging
import pandas as pd
from opentelemetry import trace
from src.config import DATA_SOURCE

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

def extract_data():
    with tracer.start_as_current_span("extract_data", attributes={"source": DATA_SOURCE}):
        try:
            df = pd.read_csv(DATA_SOURCE)
            logger.info("Data extracted from %s", DATA_SOURCE)
            return df
        except Exception as e:
            logger.exception("Error extracting data: %s", e)
            return pd.DataFrame()
    
