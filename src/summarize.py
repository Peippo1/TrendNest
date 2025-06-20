import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

def generate_summary(df):
    print("🧠 Generating summary with Gemini 1.5...")
    prompt = f"Summarize recent stock trends from this data:\n{df.to_markdown(index=False)}"
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"⚠️ Gemini summarization failed: {e}")
        return "Summary unavailable due to API error."
