import os
import pandas_gbq
from google.oauth2 import service_account

# Configuration
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "")
DATASET = os.getenv("BQ_DATASET", "trendnest")
TABLE = os.getenv("BQ_TABLE", "cleaned_stock_data")

def upload_to_bigquery(df):
    print("🚀 Uploading data to BigQuery...")

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

    print("📋 Column types and names:")
    print(df.columns.tolist()) # type: ignore
    print("✅ Columns are strings:", all(isinstance(col, str) for col in df.columns))

    
    try:
        pandas_gbq.to_gbq(
            dataframe=df,
            destination_table=f"{DATASET}.{TABLE}",
            project_id=PROJECT_ID,
            if_exists="append"
        )
        print(f"✅ Upload to BigQuery complete: {DATASET}.{TABLE}")
    except Exception as e:
        print(f"❌ Failed to upload to BigQuery: {e}")
