import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import plotly.express as px
from src.extract import extract_data
from src.transform import clean_data
from src.model import analyze_trends
from src.summarize import generate_summary

st.set_page_config(page_title="TrendNest Dashboard", layout="wide")

st.title("📈 TrendNest Dashboard")
st.markdown("Visualize and summarize trends in your data using AI-powered insights.")

# Step 1: Load and show raw data
st.header("1. Raw Data")
df_raw = extract_data()
st.dataframe(df_raw, use_container_width=True)

# Step 2: Clean data
st.header("2. Cleaned Data")
df_clean = clean_data(df_raw)
st.dataframe(df_clean, use_container_width=True)

# Step 3: Trend analysis
st.header("3. Trend Summary")
trend_summary = analyze_trends(df_clean)
st.dataframe(trend_summary, use_container_width=True)

# Step 4: AI Summary
st.header("4. AI-Generated Insight")
summary = generate_summary(trend_summary)
st.success(summary)

# Step 4: Explore Other Chart Options
st.header("4. Explore Additional Charts")

if 'date' in df_clean.columns and 'value' in df_clean.columns:
    # Grouping options
    group_freq = st.selectbox("Group data by", options=["Daily", "Weekly", "Monthly"])
    df_clean.set_index('date', inplace=True)
    if group_freq == "Weekly":
        df_grouped = df_clean['value'].resample('W').mean().reset_index()
    elif group_freq == "Monthly":
        df_grouped = df_clean['value'].resample('M').mean().reset_index()
    else:
        df_grouped = df_clean.reset_index()

    chart_type = st.radio("Choose chart type", options=["Bar", "Area", "Histogram"], horizontal=True)

    if chart_type == "Bar":
        fig = px.bar(df_grouped, x='date', y='value', title="Bar Chart of Values Over Time")
    elif chart_type == "Area":
        fig = px.area(df_grouped, x='date', y='value', title="Area Chart of Values Over Time")
    elif chart_type == "Histogram":
        fig = px.histogram(df_grouped, x='value', nbins=10, title="Histogram of Values")

    fig.update_traces(hovertemplate='Date: %{x}<br>Value: %{y}')
    fig.update_layout(xaxis_title="Date", yaxis_title="Value", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

# Optional: Download cleaned data
csv = df_clean.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Cleaned Data as CSV",
    data=csv,
    file_name="cleaned_data.csv",
    mime="text/csv"
)