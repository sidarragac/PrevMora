from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ....config.database import get_db_session
from ....controllers.payment import PaymentController
from ....schemas.Payment import (
    PaymentInitializationRequest,
    PaymentInitializationResponse,
)

router = APIRouter()


@router.post(
    "/initialize_payment",
    response_model=PaymentInitializationResponse,
    tags=["Payments"],
    summary="Initialize a payment session and auto-process payment",
    description=(
        "Initialize a payment by getting client credit details, creating a payment session "
        "in the external payment gateway, and automatically marking all pending installments as paid. "
        "Returns a payment URL to redirect the user."
    ),
)
async def initialize_payment(
    payment_request: PaymentInitializationRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Initialize a payment session for a client and automatically process payment.

    This endpoint:
    1. Fetches the client's credit details from the database
    2. Sends the credit information to the external payment gateway
    3. **Automatically marks all pending/overdue installments as "Pagada"**
    4. Sets payment_date to today for each installment
    5. Creates reconciliation records for each installment
    6. Updates credit state to "Pagado" if all installments are paid
    7. Returns a payment URL where the user can view the payment confirmation

    Args:
        payment_request: Request containing client_id and optional credit_id
        session: Database session (injected)

    Returns:
        PaymentInitializationResponse: Contains payment URL and session information

    Example:
        ```json
        {
            "client_id": 1,
            "credit_id": 6
        }
        ```

    Response:
        ```json
        {
            "success": true,
            "sessionId": "SESSION_1730828400_abc123xyz",
            "paymentUrl": "https://payment-gateway3-beige.vercel.app?session=SESSION_1730828400_abc123xyz",
            "expiresIn": 1800,
            "message": "Payment session created. Redirect user to paymentUrl"
        }
        ```
    """
    controller = PaymentController()
    return await controller.initialize_payment(session, payment_request)
