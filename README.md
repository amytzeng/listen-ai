# Listen AI - Social Listening Platform

A lightweight multi-service social listening platform with:

- Streamlit frontend dashboard
- Node.js gateway for auth and API orchestration
- Python NLP service for sentiment analysis
- Go statistics service for keyword and trend analytics
- SQLite database for post storage

## Architecture

- `frontend` (Streamlit): user input and dashboard rendering
- `gateway` (Node.js): authentication and request routing/composition
- `nlp` (Python/FastAPI): sentiment detection from post text
- `stat` (Go): mentions, trends, top keywords, post retrieval
- `db` (SQLite): stored under `./data/listenai.db`

## API Summary

### Gateway

- `POST /auth/login`
- `POST /api/dashboard` (Bearer token required)

### Stat

- `POST /stats`
- `GET /health`

### NLP

- `POST /sentiment`
- `GET /health`

## Manual local run (without Docker)

Use four terminals:

1. Stat service
```bash
cd stat
go mod tidy
go run .
```

2. NLP service
```bash
cd nlp
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8001
```

3. Gateway service
```bash
cd gateway
npm install
npm run dev
```

4. Frontend
```bash
cd frontend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.port 8501
```
