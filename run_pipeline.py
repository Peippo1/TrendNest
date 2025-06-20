from src.extract_stocks import fetch_stock_data_yf
from src.transform import clean_data
from src.model import analyze_trends
from src.summarize import generate_summary
from src.export import export_to_csv
from src.config import EXPORT_PATH, STOCK_SYMBOL
from src.upload import upload_to_bigquery

def main():
    print("🚀 Starting TrendNest pipeline...\n")

    # Extract
    symbol = STOCK_SYMBOL or "AAPL"
    print(f"📥 Fetching live stock data for: {symbol}")
    df_raw = fetch_stock_data_yf(symbol)
    print(f"✅ Fetched live stock data for {symbol} — {len(df_raw)} rows")
    if df_raw.empty:
        print("❌ No data extracted. Exiting pipeline.")
        return

    # Transform
    df_clean = clean_data(df_raw)
    df_clean["Ticker"] = symbol

    # Analyze
    trend_output = analyze_trends(df_clean)

    # Summarize
    summary = generate_summary(trend_output)
    print(f"\n📋 AI Summary:\n{summary}\n")

    # Ticker
    df_clean["Ticker"] = symbol
    
    # Export
    export_to_csv(df_clean, EXPORT_PATH)

    upload_to_bigquery(df_clean)

    print("\n✅ Pipeline complete.")

if __name__ == "__main__":
    main()
