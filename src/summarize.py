import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

def generate_summary(df):
    print("🧠 Generating summary with Gemini 1.5...")
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
        print(f"⚠️ Gemini summarization failed: {e}")
        return "Summary unavailable due to API error."
