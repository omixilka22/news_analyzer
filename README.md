# 📰 News Sentiment Analyzer

An end-to-end data pipeline that scrapes Ukrainian news articles, stores them in PostgreSQL, and performs sentiment analysis using a multilingual NLP model. Built as a Data Analyst portfolio project.

---

## 🚀 Features

- **Web scraping** — collects news articles from unian.ua using BeautifulSoup
- **PostgreSQL storage** — saves articles via psycopg2 with deduplication
- **Sentiment analysis** — classifies articles as positive / negative / neutral using HuggingFace Transformers (`cardiffnlp/twitter-xlm-roberta-base-sentiment`)
- **Automated scheduler** — refreshes data every 6 hours, skips if data is already fresh
- **Interactive dashboard** — Streamlit app with filters, metrics, charts, and manual refresh
- **Docker** — fully containerized with docker-compose (app + scheduler + PostgreSQL)

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Scraping | Python, requests, BeautifulSoup4, lxml |
| Storage | PostgreSQL, psycopg2 |
| NLP | HuggingFace Transformers, PyTorch (CPU) |
| Analysis | pandas, matplotlib, seaborn |
| Dashboard | Streamlit |
| Scheduling | schedule |
| Infrastructure | Docker, docker-compose |

---

## 📁 Project Structure

```
NewsAnalyzer/
├── analysis/
│   ├── sentiment.py      # HuggingFace sentiment pipeline
│   ├── trends.py         # top words, sentiment stats, daily stats
│   └── visualize.py      # matplotlib/seaborn charts
├── dashboard/
│   └── app.py            # Streamlit dashboard
├── db/
│   ├── connection.py     # psycopg2 connection
│   ├── repository.py     # insert/select functions
│   └── schemas.sql       # table definitions
├── scrapy/
│   ├── model.py          # Article dataclass
│   └── scraper.py        # unian.ua scraper
├── main.py               # manual run script
├── scheduler.py          # automated data collection
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── requirements.txt
```

---

## ⚙️ Setup

### Prerequisites

- Docker and Docker Compose installed
- HuggingFace account (free) for model access

### 1. Clone the repository

```bash
git clone https://github.com/omixilka22/news_analyzer.git
cd news_analyzer
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Fill in your `.env`:

```
DB_NAME=news_analyzer
DB_USER=your_db_user
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432
HF_TOKEN=your_huggingface_token
```

### 3. Run with Docker

```bash
docker-compose up --build
```

This starts three services:
- `db` — PostgreSQL database
- `scheduler` — collects and analyzes news every 6 hours
- `app` — Streamlit dashboard on port 8501

### 4. Open the dashboard

```
http://localhost:8501
```

---

## 🔄 How It Works

```
unian.ua
   │
   ▼
scraper.py          ← BeautifulSoup parses articles
   │
   ▼
repository.py       ← psycopg2 inserts into PostgreSQL
   │
   ▼
sentiment.py        ← HuggingFace classifies sentiment
   │
   ▼
dashboard/app.py    ← Streamlit visualizes results
```

The scheduler checks whether the latest article in the database is older than 1 hour before triggering a new scrape, avoiding unnecessary requests.

---

## 📊 Dashboard

The Streamlit dashboard includes:

- **Metrics** — total articles, breakdown by sentiment
- **Articles table** — filterable by sentiment (positive / negative / neutral)
- **Sentiment distribution** — bar chart
- **Top words** — most frequent words in headlines
- **Daily dynamics** — line chart of articles per day by sentiment
- **Manual refresh** — button to trigger data collection on demand

---

## 🗄 Database Schema

```sql
CREATE TABLE articles (
    id          SERIAL PRIMARY KEY,
    title       TEXT NOT NULL,
    url         TEXT UNIQUE NOT NULL,
    source      VARCHAR(100) NOT NULL,
    published_at TIMESTAMP NOT NULL,
    content     TEXT NOT NULL,
    description TEXT,
    sentiment   VARCHAR(50)
);
```

---

## 🤖 NLP Model

Uses [`cardiffnlp/twitter-xlm-roberta-base-sentiment`](https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base-sentiment) — a multilingual XLM-RoBERTa model fine-tuned on ~198M tweets across 100+ languages including Ukrainian.

---

## 📝 Running Without Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run once
python main.py

# Run dashboard
streamlit run dashboard/app.py
```

---
