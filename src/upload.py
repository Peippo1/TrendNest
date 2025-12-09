import logging
import os
import pandas_gbq
from google.oauth2 import service_account
from opentelemetry import trace

# Configuration
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "")
DATASET = os.getenv("BQ_DATASET", "trendnest")
TABLE = os.getenv("BQ_TABLE", "cleaned_stock_data")

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


def upload_to_bigquery(df):
    with tracer.start_as_current_span(
        "upload_to_bigquery",
        attributes={"project_id": PROJECT_ID, "dataset": DATASET, "table": TABLE},
    ):
        logger.info("Uploading data to BigQuery")

        # Authenticate using service account
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path or not os.path.isfile(credentials_path):
            raise EnvironmentError("Missing or invalid GOOGLE_APPLICATION_CREDENTIALS path.")

        credentials = service_account.Credentials.from_service_account_file(credentials_path)

        # Set global context for pandas_gbq
        pandas_gbq.context.credentials = credentials
        pandas_gbq.context.project = PROJECT_ID

        # Flatten column headers in case of MultiIndex
        df.columns = [col[0] if isinstance(col, tuple) else str(col) for col in df.columns]

        logger.debug("Column names: %s", df.columns.tolist())  # type: ignore
        logger.debug("Columns are strings: %s", all(isinstance(col, str) for col in df.columns))

        try:
            pandas_gbq.to_gbq(
                dataframe=df,
                destination_table=f"{DATASET}.{TABLE}",
                project_id=PROJECT_ID,
                if_exists="append"
            )
            logger.info("Upload to BigQuery complete: %s.%s", DATASET, TABLE)
        except Exception as e:
            logger.exception("Failed to upload to BigQuery: %s", e)
            raise
