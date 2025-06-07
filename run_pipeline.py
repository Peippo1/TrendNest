from src.extract import extract_data
from src.transform import clean_data
from src.model import analyze_trends
from src.summarize import generate_summary
from src.export import export_to_csv
from src.config import EXPORT_PATH

def main():
    print("🚀 Starting TrendNest pipeline...\n")

    # Extract
    df_raw = extract_data()
    if df_raw.empty:
        print("❌ No data extracted. Exiting pipeline.")
        return

    # Transform
    df_clean = clean_data(df_raw)

    # Analyze
    trend_output = analyze_trends(df_clean)

    # Summarize
    summary = generate_summary(trend_output)
    print(f"\n📋 AI Summary:\n{summary}\n")

    # Export
    export_to_csv(df_clean, EXPORT_PATH)

    print("\n✅ Pipeline complete.")

if __name__ == "__main__":
    main()
