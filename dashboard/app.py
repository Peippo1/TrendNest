import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="TrendNest Dashboard", layout="wide")

st.title("📊 TrendNest: Stock Data Dashboard")

DATA_PATH = os.getenv("EXPORT_PATH", "data/cleaned_data.csv")

# Load data
try:
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    st.success("✅ Data loaded successfully.")
except FileNotFoundError:
    st.error("❌ Data file not found. Please run the pipeline first.")
    st.stop()

# Dropdown for ticker (prepare for multi-ticker later)
ticker = st.selectbox("Select Ticker", options=[df["Ticker"].iloc[0]], index=0)


# Filtered data
filtered_df = df[df["Ticker"] == ticker]

# Date range filter
if filtered_df.empty or filtered_df["date"].isna().all():
    st.warning("⚠️ No valid dates available for this ticker.")
    st.stop()

min_date = filtered_df["date"].min().date()
max_date = filtered_df["date"].max().date()

date_range = st.slider(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

filtered_df = filtered_df[
    (filtered_df["date"].dt.date >= date_range[0]) &
    (filtered_df["date"].dt.date <= date_range[1])
]

# Charts
st.subheader("📈 Adjusted Close Price")
st.line_chart(filtered_df.set_index("date")["adjusted_close"])

st.subheader("📊 Volume")
st.bar_chart(filtered_df.set_index("date")["volume"])


# Summary placeholder
st.subheader("🧠 AI Summary")
st.info("This is a placeholder summary from Gemini 1.5. Replace with live model output later.")

# Download button
st.subheader("📥 Download Data")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("Download Filtered CSV", data=csv, file_name=f"{ticker}_filtered_data.csv", mime="text/csv")
