import logging
import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
from opentelemetry import trace

from src.config import get_settings

load_dotenv()

settings = get_settings()
genai.configure(api_key=settings.gemini_api_key or os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

def generate_summary(df):
    with tracer.start_as_current_span("generate_summary"):
        logger.info("Generating summary with Gemini 1.5")
        # Clean potentially erroneous rows
        df = df[(df["Close"] > 0) & (df["Volume"] > 0)].copy()
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        df = df.sort_values("date").reset_index(drop=True)

        # Optionally remove first and last rows if enough data is present
        if len(df) > 4:
            df = df.iloc[1:-1]

        prompt = f"Summarize recent stock trends from this data:\n{df.to_markdown(index=False)}"

        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.exception("Gemini summarization failed: %s", e)
            return "Summary unavailable due to API error."
