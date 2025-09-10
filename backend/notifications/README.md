# PrevMora Notifications Microservice

A lightweight FastAPI microservice that provides notification data for clients with alerts.

## Features

- Single endpoint to retrieve client alert notification data
- Retrieves phone, name, installment value, and payment date for clients in the Alert table
- Joins Alert, Client, Credit, and Installment tables
- Returns formatted JSON response ready for notifications

## API Endpoint

### GET `/api/notifications/v1/client-alerts`

Returns client notification data in the following format:

```json
[
    {"to": "+573007465380", "name": "Alejo", "amount": "200.000", "date": "2025-09-20"},
    {"to": "+573012706204", "name": "Wambi", "amount": "200.000", "date": "2025-09-05"},
    {"to": "+573174929988", "name": "Santi idarraga", "amount": "200.000", "date": "2025-09-20"},
    {"to": "+573007881347", "name": "Wambi", "amount": "200.000", "date": "2025-09-20"}
]
```

**Response Fields:**
- `to`: Client phone number
- `name`: Client name
- `amount`: Installment value formatted with thousands separator
- `date`: Payment date in YYYY-MM-DD format

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (copy from credit_management service)

3. Run the service:
```bash
uvicorn app.main:app --reload --port 8001
```

## Database

Uses the same database as the credit_management service. The endpoint queries:
- Alert table (to identify clients with alerts)
- Client table (for phone and name)
- Credit table (to link alerts to installments)
- Installment table (for installment value and payment date)

## Documentation

Once running, access interactive API documentation at:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc
