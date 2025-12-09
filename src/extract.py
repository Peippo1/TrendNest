import logging
import pandas as pd
from opentelemetry import trace
from src.config import get_settings

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

def extract_data():
    settings = get_settings()
    with tracer.start_as_current_span("extract_data", attributes={"source": settings.data_source}):
        try:
            df = pd.read_csv(settings.data_source)
            logger.info("Data extracted from %s", settings.data_source)
            return df
        except Exception as e:
            logger.exception("Error extracting data: %s", e)
            return pd.DataFrame()
    
