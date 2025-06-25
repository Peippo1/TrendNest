from src.extract_stocks import fetch_stock_data_yf
from src.transform import clean_data
from src.model import analyze_trends
from src.summarize import generate_summary
from src.export import export_to_csv
from src.config import EXPORT_PATH, get_top_performing_stocks
from src.upload import upload_to_bigquery
import pandas as pd

def main():
    print("🚀 Starting TrendNest pipeline...\n")

    tickers = get_top_performing_stocks()
    print(f"🧾 Tickers to process: {', '.join(tickers)}")

    combined_df = []

    for symbol in tickers:
        print(f"\n📥 Fetching live stock data for: {symbol}")
        df_raw = fetch_stock_data_yf(symbol)
        if df_raw is None or df_raw.empty:
            print(f"❌ No data for {symbol}. Skipping.")
            continue

        print(f"✅ Fetched live stock data for {symbol} — {len(df_raw)} rows")

        # Transform
        df_clean = clean_data(df_raw)
        df_clean["Ticker"] = symbol

        # Analyze
        trend_output = analyze_trends(df_clean)

        # Summarize
        summary = generate_summary(trend_output)
        print(f"\n📋 AI Summary ({symbol}):\n{summary}\n")

        print(f"📋 Columns for {symbol}: {df_clean.columns.tolist()}")
        combined_df.append(df_clean)

    if combined_df:
        full_df = pd.concat(combined_df, ignore_index=True)
        export_to_csv(full_df, EXPORT_PATH)
        upload_to_bigquery(full_df)

    print("\n✅ Pipeline complete.")

if __name__ == "__main__":
    main()
