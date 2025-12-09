# TrendNest

| ![Repo Size](https://img.shields.io/github/repo-size/Peippo1/TrendNest) | ![Last Commit](https://img.shields.io/github/last-commit/Peippo1/TrendNest) | ![License](https://img.shields.io/github/license/Peippo1/TrendNest) | ![Python Version](https://img.shields.io/badge/python-3.10%2B-blue) | ![Build](https://img.shields.io/badge/build-passing-brightgreen) | ![Docker](https://img.shields.io/badge/docker-ready-blue) | ![GCP](https://img.shields.io/badge/GCP-BigQuery-informational) | ![Gemini](https://img.shields.io/badge/Gemini-1.5_AI-yellow) | ![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b?logo=streamlit&logoColor=white) |
|:------------------------------------------------------------------------:|:-----------------------------------------------------------------------------:|:--------------------------------------------------------------------:|:------------------------------------------------------------------:|:--------------------------------------------------------------:|:--------------------------------------------------------:|:----------------------------------------------------:|:--------------------------------------------------:|:--------------------------------------------------:|
| Repo size                                                               | Last commit                                                                  | License                                                              | Python version                                                    | Build status                                                  | Docker support                                        | GCP BigQuery                                         | Gemini AI summarization                           | Streamlit App                                    |

**TrendNest** is a portfolio-ready data pipeline and dashboard project that ingests, transforms, models, and visualizes data trends over time. It integrates AI summarization using Gemini 1.5 and supports exporting cleaned data to CSV. The project is fully containerized and deployable.

## 🔧 Features

- Data extraction from various sources (e.g. APIs, databases, files)
- Transformation pipeline via configurable "recipe"
- Time-based trend modeling
- AI-generated summaries using Gemini 1.5
- Interactive dashboard built with Streamlit (or Dash)
- CSV downloads of processed data
- Dockerized for deployment

## 🗂 Project Structure

```
TrendNest/
├── dags/                      # Airflow DAGs (optional)
├── dashboard/                 # Streamlit dashboard app
│   └── app.py                 # Main UI script
├── data/                      # Local and processed data
│   ├── cleaned_data.csv       # Output from pipeline
│   └── sample.csv             # Example input data
├── docker/                    # Containerization setup
│   └── Dockerfile             # Docker build instructions
├── docs/                      # Documentation and notes
│   └── design.md              # System design outline
├── notebooks/                 # Jupyter notebooks (EDA, prototyping)
├── sql/                       # BigQuery-compatible SQL queries
│   ├── monthly_averages.sql   # Avg monthly close/volume
│   ├── latest_prices.sql      # Most recent close prices
│   └── volume_spikes.sql      # High-volume trading days
├── src/                       # Core data pipeline logic
│   ├── __init__.py
│   ├── config.py              # Config constants
│   ├── extract.py             # Local/CSV data extraction
│   ├── extract_stocks.py      # YFinance stock extractor
│   ├── transform.py           # Data cleaning
│   ├── model.py               # Trend modeling
│   ├── summarize.py           # Gemini AI summaries
│   ├── export.py              # CSV export
│   └── upload.py              # BigQuery uploader
├── test_https.py              # API connectivity test
├── test_upload.py             # BigQuery upload test
├── test_yfinance_fetch.py     # yfinance fetch test
├── tests/                     # Unit tests (placeholder)
├── run_pipeline.py            # Main pipeline runner
├── requirements.txt           # Python dependencies
├── .env.example               # Sample environment variables (copy to .env)
├── .gitignore                 # Git exclusions
└── README.md                  # This file
```

## 🚀 Getting Started

1. Clone the repo:
   ```
   git clone https://github.com/yourusername/TrendNest.git
   cd TrendNest
   ```

2. Set up your environment:
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env`, then fill in your own credentials. Keep `.env` out of version control.

4. (Optional) Set up observability:
   - `LOG_LEVEL` controls verbosity (default `INFO`).
   - To emit OpenTelemetry traces/metrics to a collector, set `OTEL_EXPORTER_OTLP_ENDPOINT` (HTTP/OTLP) and optional `OTEL_EXPORTER_OTLP_HEADERS` for auth. Without it, spans are printed to stdout and metrics stay local.
   - `ENVIRONMENT` tags spans/metrics (e.g., `dev`, `staging`, `prod`).
   - `TOP_PERFORMERS_LIMIT` and `TICKERS_UNIVERSE` let you tune the ticker selection.
   - Resilience knobs: `MAX_WORKERS`, `FETCH_TIMEOUT_SECONDS`, `FETCH_MAX_RETRIES`, `FETCH_BACKOFF_SECONDS`, and `DEAD_LETTER_PATH` for failed rows.

5. Run the pipeline:
   ```
   python run_pipeline.py
   ```

6. Start the dashboard:
   ```
   streamlit run dashboard/app.py
   ```

Command-line overrides:
```
python run_pipeline.py --tickers AAPL,MSFT --limit 5 --export-path /tmp/output.csv --dead-letter-path /tmp/failed.csv
```

## 🔍 Observability + metrics
- Tracing: pipeline run → per-ticker spans + downstream HTTP (requests/yfinance) via OpenTelemetry.
- Metrics: counters for runs, tickers processed, and rows processed (`trendnest.pipeline.*`). They export via OTLP if configured, else stay in-process.
- Logs: structured `logging` with `run_id` on key entries; adjust `LOG_LEVEL` as needed.
- Resilience: bounded retries with jitter, timeouts on fetches, concurrent ticker processing (`MAX_WORKERS`), and a dead-letter CSV for failures.

## 🧠 AI Summarization (Gemini 1.5)

TrendNest integrates Gemini 1.5 to generate natural language summaries of key insights in your trend data. This makes the dashboard useful to both technical and non-technical stakeholders.

Example summary output:
> "Apple's stock (AAPL) shows a general upward trend from December 2024 to June 2025, increasing from ~$172 to ~$258. Trading volume spiked in June, suggesting heightened investor interest."

## 🗃️ BigQuery Integration

TrendNest supports uploading cleaned trend data to Google BigQuery. This enables:
- SQL-based analysis
- Historical trend aggregation
- Integration with Looker Studio or other BI tools

Each run appends to the `trendnest.cleaned_stock_data` table using a service account key.

## 🧮 SQL Querying Example

Once data is in BigQuery, you can run SQL like:

```sql
SELECT
  FORMAT_DATE('%Y-%m', PARSE_DATE('%Y-%m-%d', date)) AS month,
  ROUND(AVG(CAST(Close AS FLOAT64)), 2) AS avg_close,
  ROUND(AVG(CAST(Volume AS INT64))) AS avg_volume
FROM `trendnest-463421.trendnest.cleaned_stock_data`
WHERE Ticker = 'AAPL'
GROUP BY month
ORDER BY month;
```

---

### 📂 Included SQL Files

The `/sql/` directory contains reusable queries for analytics and dashboarding:

- `monthly_averages.sql`: Calculates average monthly closing price and trading volume
- `latest_prices.sql`: Retrieves the most recent closing price for each ticker
- `volume_spikes.sql`: Identifies unusually high trading volume days

These can be run in BigQuery or loaded into the dashboard for insights.

---

## 🐳 Docker Support

Build and run the container:

```
docker build -t trendnest .
docker run -p 8501:8501 trendnest
```

## 📄 License

MIT — free to use, modify, and distribute.

## 📦 Changelog

### v1.1.0
- Integrated Gemini 1.5 for AI-generated summaries
- Implemented BigQuery upload via service account
- Enabled SQL querying and Looker Studio compatibility

### v1.2.0
- Multi-ticker support added with interactive dashboard controls
- Upgraded Streamlit dashboard with Altair charts (line and bar)
- Dynamic filtering and AI summaries per selected ticker
- Enhanced CSV export for selected tickers and date ranges
- Improved dashboard responsiveness and readability
