# 🧠 TrendNest Design Document

This document outlines the architectural design, component breakdown, and roadmap for the TrendNest data pipeline and dashboard application.

---

## 🎯 Project Overview

**TrendNest** is a modular data platform that:
- Ingests time-series or structured data
- Applies transformation recipes (cleaning, sorting)
- Analyzes trends over time
- Summarizes insights using Gemini 1.5
- Visualizes the output via an interactive dashboard

---

## 🧱 Architecture

**Languages & Tools**: Python, SQL, Streamlit, Plotly, BigQuery (optional), Docker  
**AI**: Gemini 1.5 integration planned  
**Storage**: Local CSV for dev; BigQuery for scalable deployments

**Core Components**:
- `src/extract.py`: Load CSVs or connect to APIs/dbs
- `src/transform.py`: Cleaning, type casting, sorting
- `src/model.py`: Trend modeling (e.g. summary stats, rolling averages)
- `src/summarize.py`: Natural language generation via Gemini
- `src/export.py`: Save to CSV
- `dashboard/app.py`: UI interface for exploration, filtering, and downloads

---

## 🧩 Dashboard Features

- Filter data by date range
- Group by day, week, or month
- Visualize trends using line, bar, area, and histogram charts
- Export cleaned data as CSV
- Placeholder AI summary (Gemini API planned)

---

## 🛣️ Future Extensions

- ✅ Connect Gemini 1.5 via secure API
- ⏳ Integrate BigQuery for data warehousing
- ⏳ Add authentication layer to dashboard (e.g., via Streamlit login)
- ⏳ Create an Airflow DAG for automated scheduling
- ⏳ Support for additional file types (e.g., JSON, Excel)
- ⏳ Model time-based forecasts using Prophet or similar

---

## 🔁 Dev Workflow

1. Create `.env` and drop sample data in `data/`
2. Run `run_pipeline.py` to test end-to-end flow
3. Use `streamlit run dashboard/app.py` to view the interface
4. Add new transformations or models modularly in `src/`
5. Push updates and tag releases

---

## ✨ Notes

This is an evolving project aimed at demonstrating full-stack data engineering and AI-integrated analytics. Simplicity, clarity, and usability are the primary goals.
