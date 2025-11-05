# PrevMora Analytics KPI Microservice

FastAPI service that exposes KPI-related analytics endpoints.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export APP_NAME="analitycs_kpi"
export DB_USER="your-user"  # and the rest of the required variables
uvicorn app.main:app --reload
```

Provide configuration through environment variables; the service no longer loads a `.env` file automatically.
