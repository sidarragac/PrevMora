## FastAPI Microservice Template

This is a reusable template for building FastAPI microservices with a clean, layered structure:

- adapters
- auth
- config
- controllers
- models
- routes
- utils
- tests

### Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### Run tests

```bash
pytest -q
```

Environment variables can be configured in `.env` (see `.env.example`).

