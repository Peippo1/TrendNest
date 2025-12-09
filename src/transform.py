import logging
from opentelemetry import trace

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

def clean_data(df):
    with tracer.start_as_current_span("clean_data"):
        # Example transformation: drop nulls and sort by date
        df_clean = df.dropna()

        # Drop duplicate columns if any
        df_clean = df_clean.loc[:, ~df_clean.columns.duplicated()]

        if 'date' in df_clean.columns:
            df_clean = df_clean.sort_values(by='date')
        logger.info("Data cleaned and sorted")
        return df_clean
