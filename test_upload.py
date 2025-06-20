import pandas as pd
from dotenv import load_dotenv
load_dotenv()

from src.upload import upload_to_bigquery

df = pd.read_csv("data/cleaned_data.csv")
upload_to_bigquery(df)