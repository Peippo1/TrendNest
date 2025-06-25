import streamlit as st
import pandas as pd
import os
import altair as alt

st.set_page_config(page_title="TrendNest Dashboard", layout="wide")

st.title("📊 TrendNest")
st.caption("Explore live stock trends and volumes with AI-powered summaries")

DATA_PATH = os.getenv("EXPORT_PATH", "data/cleaned_data.csv")

# Load data
try:
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    st.success("✅ Data loaded successfully.")
except FileNotFoundError:
    st.error("❌ Data file not found. Please run the pipeline first.")
    st.stop()

tickers = df["Ticker"].dropna().unique().tolist()

selected_tickers = st.multiselect("Select Tickers", options=tickers, default=tickers[:5])

if not selected_tickers:
    st.warning("⚠️ Please select at least one ticker.")
    st.stop()

# Filtered data
filtered_df = df[df["Ticker"].isin(selected_tickers)]

# Date range filter
if filtered_df.empty or filtered_df["date"].isna().all():
    st.warning("⚠️ No valid dates available for the selected tickers.")
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
line_chart = alt.Chart(filtered_df.tail(300)).mark_line().encode(
    x="date:T",
    y="Close:Q",
    color="Ticker:N",
    tooltip=["Ticker", "date", "Close"]
).properties(width=800, height=400)
st.altair_chart(line_chart, use_container_width=True)

st.subheader("📊 Volume")
bar_chart = alt.Chart(filtered_df.tail(300)).mark_bar().encode(
    x="date:T",
    y="Volume:Q",
    color="Ticker:N",
    tooltip=["Ticker", "date", "Volume"]
).properties(width=800, height=400)
st.altair_chart(bar_chart, use_container_width=True)

st.subheader("🧠 AI Summaries")
for ticker in selected_tickers:
    ticker_df = filtered_df[filtered_df["Ticker"] == ticker]
    if "summary" in ticker_df.columns and not ticker_df["summary"].isna().all():
        summary_text = ticker_df["summary"].dropna().iloc[-1]
        st.markdown(f"**{ticker}**")
        st.success(summary_text)
    else:
        st.markdown(f"**{ticker}**")
        st.info("No AI summary available.")

# Download button
st.subheader("📥 Download Data")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("Download Filtered CSV", data=csv, file_name="filtered_stock_data.csv", mime="text/csv")
