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
export APP_NAME="payments"  # ...and other required variables
uvicorn app.main:app --reload
```

### Run tests

```bash
pytest -q
```

Environment variables should be provided directly through your shell or orchestration environment.

### Payment Gateway Integration

This microservice includes integration with an external payment gateway for processing client payments.

#### Payment Initialization Endpoint

**Endpoint:** `POST /api/{APP_NAME}/v1/payments/initialize_payment`

Note: Replace `{APP_NAME}` with the value configured in your environment (e.g., `APP_NAME=payments`)

**Description:** Initializes a payment session by fetching client credit details, creating a payment session in the external payment gateway, and **automatically processing the payment** by marking all pending installments as paid.

**Request Body:**
```json
{
  "client_id": 1,
  "credit_id": 6  // Optional: if not provided, the first credit will be used
}
```

**Response:**
```json
{
  "success": true,
  "sessionId": "SESSION_1730828400_abc123xyz",
  "paymentUrl": "https://payment-gateway3-beige.vercel.app?session=SESSION_1730828400_abc123xyz",
  "expiresIn": 1800,
  "message": "Payment session created. Redirect user to paymentUrl"
}
```

**Usage Flow:**
1. Frontend sends a POST request with `client_id` (and optionally `credit_id`)
2. Backend fetches credit details from `/get_credits_detailed/{client_id}`
3. Backend sends credit data to external payment gateway at `https://payment-gateway3-beige.vercel.app/api/initialize-payment`
4. **Backend automatically processes payment:**
   - Marks all pending/overdue installments as "Pagada"
   - Sets payment_date to today
   - Creates reconciliation records
   - Updates credit state to "Pagado" if all installments are paid
5. Backend returns the payment URL to the frontend
6. Frontend redirects the user to the `paymentUrl` where they can view the payment confirmation

**Error Responses:**
- `404`: Client or credit not found
- `400`: Payment gateway returned an error
- `503`: Failed to connect to payment gateway
- `500`: Unexpected internal error

#### Implementation Details

The payment integration consists of:
- **Schema:** `app/schemas/Payment.py` - Request/response models
- **Controller:** `app/controllers/payment.py` - Business logic for payment initialization
- **Routes:** `app/api/routes/v1/payment.py` - API endpoint definition

The integration uses the `httpx` library for async HTTP requests to the external payment gateway.

