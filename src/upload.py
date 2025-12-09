import logging
import os
import pandas_gbq
from google.oauth2 import service_account
from opentelemetry import trace

from src.config import get_settings

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


def upload_to_bigquery(df):
    settings = get_settings()
    with tracer.start_as_current_span(
        "upload_to_bigquery",
        attributes={
            "project_id": settings.gcp_project_id,
            "dataset": settings.bq_dataset,
            "table": settings.bq_table,
        },
    ):
        logger.info("Uploading data to BigQuery")

        # Authenticate using service account
        credentials_path = settings.google_credentials_path or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path or not os.path.isfile(credentials_path):
            raise EnvironmentError("Missing or invalid GOOGLE_APPLICATION_CREDENTIALS path.")

        credentials = service_account.Credentials.from_service_account_file(credentials_path)

        # Set global context for pandas_gbq
        pandas_gbq.context.credentials = credentials
        pandas_gbq.context.project = settings.gcp_project_id

        # Flatten column headers in case of MultiIndex
        df.columns = [col[0] if isinstance(col, tuple) else str(col) for col in df.columns]

        logger.debug("Column names: %s", df.columns.tolist())  # type: ignore
        logger.debug("Columns are strings: %s", all(isinstance(col, str) for col in df.columns))

        try:
            pandas_gbq.to_gbq(
                dataframe=df,
                destination_table=f"{settings.bq_dataset}.{settings.bq_table}",
                project_id=settings.gcp_project_id,
                if_exists="append"
            )
            logger.info("Upload to BigQuery complete: %s.%s", settings.bq_dataset, settings.bq_table)
        except Exception as e:
            logger.exception("Failed to upload to BigQuery: %s", e)
            raise
