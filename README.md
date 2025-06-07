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
├── data/                  # Local or sample data
├── dags/                  # Airflow DAGs (optional)
├── notebooks/             # EDA and exploration
├── src/                   # Core logic
│   ├── extract.py         # Ingest data
│   ├── transform.py       # Clean and prepare
│   ├── model.py           # Trend analysis
│   ├── summarize.py       # Gemini summaries
│   └── export.py          # CSV export
├── sql/                   # SQL query files
├── dashboard/             # UI app (e.g., Streamlit)
├── tests/                 # Unit tests
├── docker/                # Dockerfile and configs
├── run_pipeline.py        # Entry point
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── .gitignore
└── README.md              # This file
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

3. Configure `.env` and update data source paths or credentials.

4. Run the pipeline:
   ```
   python run_pipeline.py
   ```

5. Start the dashboard:
   ```
   streamlit run dashboard/app.py
   ```

## 🧠 AI Summarization (Gemini 1.5)

TrendNest integrates Gemini 1.5 to generate natural language summaries of key insights in your trend data. This makes the dashboard useful to both technical and non-technical stakeholders.

## 🐳 Docker Support

Build and run the container:

```
docker build -t trendnest .
docker run -p 8501:8501 trendnest
```

## 📄 License

MIT — free to use, modify, and distribute.