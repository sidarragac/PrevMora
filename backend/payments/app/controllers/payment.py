import datetime

import httpx
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..controllers.client import ClientController
from ..models.Credit import Credit
from ..models.Installment import Installment
from ..models.Reconciliation import Reconciliation
from ..schemas.Payment import (
    PaymentInitializationRequest,
    PaymentInitializationResponse,
)


class PaymentController:
    """Controller for Payment operations."""

    PAYMENT_GATEWAY_URL = (
        "https://payment-gateway3-beige.vercel.app/api/initialize-payment"
    )

    def __init__(self):
        self.client_controller = ClientController()

    async def initialize_payment(
        self, session: AsyncSession, payment_request: PaymentInitializationRequest
    ) -> PaymentInitializationResponse:
        """
        Initialize a payment by getting credit details and sending to payment gateway.

        After successfully creating the payment session, this method automatically:
        - Marks all pending/overdue installments as "Pagada"
        - Sets payment_date to today
        - Creates reconciliation records for each installment
        - Updates credit state to "Pagado" if all installments are paid

        Args:
            session: Database session
            payment_request: Payment initialization request with client_id

        Returns:
            PaymentInitializationResponse with payment URL and session ID

        Raises:
            HTTPException: If credits not found or payment gateway fails
        """
        # Get credits detailed for the client
        try:
            credits_data = await self.client_controller.get_credits_detailed(
                session, payment_request.client_id
            )
        except HTTPException as e:
            raise HTTPException(
                status_code=404, detail=f"Failed to get credit details: {e.detail}"
            )

        # If a specific credit_id is provided, filter to that credit only
        if payment_request.credit_id:
            credits_data = [
                credit
                for credit in credits_data
                if credit.id == payment_request.credit_id
            ]
            if not credits_data:
                raise HTTPException(
                    status_code=404,
                    detail=f"Credit with ID {payment_request.credit_id} not found for this client",
                )

        # If there's only one credit, send it directly. Otherwise, send the first one
        # (You might want to adjust this logic based on business requirements)
        if len(credits_data) == 0:
            raise HTTPException(
                status_code=404, detail="No credits found for this client"
            )

        # Use the first credit (or you can modify logic to handle multiple credits)
        credit_to_send = credits_data[0]

        # Convert the credit data to the format expected by the payment gateway
        payment_data = self._convert_to_payment_gateway_format(credit_to_send)

        # Send request to payment gateway
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.PAYMENT_GATEWAY_URL, json=payment_data
                )

                if response.status_code != 200:
                    error_detail = (
                        response.json() if response.text else {"error": "Unknown error"}
                    )
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Payment gateway error: {error_detail}",
                    )

                response_data = response.json()

                if not response_data.get("success"):
                    raise HTTPException(
                        status_code=400,
                        detail=f"Payment gateway returned error: {response_data.get('error', 'Unknown error')}",
                    )

                # Automatically process payment for all pending installments
                await self._auto_process_pending_installments(
                    session, credit_to_send.id, credit_to_send.payment_reference
                )

                return PaymentInitializationResponse(**response_data)

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Failed to connect to payment gateway: {str(e)}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error initializing payment: {str(e)}",
            )

    def _convert_to_payment_gateway_format(self, credit_data) -> dict:
        """
        Convert internal credit data format to payment gateway expected format.

        Args:
            credit_data: CreditCalculatedInstallmentResponse object

        Returns:
            Dictionary in payment gateway format
        """
        # Convert installments to the required format
        installments = []
        for installment in credit_data.installments:
            installment_dict = {
                "id": installment.id,
                "credit_id": installment.credit_id,
                "installment_state": installment.installment_state,
                "installments_number": installment.installments_number,
                "installments_value": str(
                    installment.installments_value
                ),  # Convert to string
                "due_date": installment.due_date.isoformat(),
                "payment_date": (
                    installment.payment_date.isoformat()
                    if installment.payment_date
                    else None
                ),
            }
            installments.append(installment_dict)

        # Build the complete payload
        payload = {
            "id": credit_data.id,
            "client_id": credit_data.client_id,
            "disbursement_amount": credit_data.disbursement_amount,
            "payment_reference": credit_data.payment_reference,
            "interest_rate": credit_data.interest_rate,
            "total_quotas": credit_data.total_quotas,
            "disbursement_date": credit_data.disbursement_date.isoformat(),
            "credit_state": credit_data.credit_state,
            "installments": installments,
            "total_paid": (
                credit_data.total_paid if credit_data.total_paid is not None else 0
            ),
            "total_pending": (
                credit_data.total_pending
                if credit_data.total_pending is not None
                else 0
            ),
        }

        return payload

    async def _auto_process_pending_installments(
        self, session: AsyncSession, credit_id: int, payment_reference: str
    ) -> None:
        """
        Automatically mark all pending installments as paid and create reconciliation records.

        This simulates a successful payment by:
        1. Finding all pending installments for the credit
        2. Updating their status to "Pagada"
        3. Setting payment_date to today
        4. Creating reconciliation records for each installment
        5. Updating credit state to "Pagado" if all installments are paid

        Args:
            session: Database session
            credit_id: ID of the credit to process
            payment_reference: Payment reference for reconciliation records

        Raises:
            HTTPException: If processing fails
        """
        try:
            # Get all pending installments for this credit
            installments_query = select(Installment).where(
                Installment.credit_id == credit_id,
                Installment.installment_state.in_(["Pendiente", "Vencida"]),
            )
            installments_result = await session.execute(installments_query)
            pending_installments = installments_result.scalars().all()

            if not pending_installments:
                # No pending installments to process
                return

            today = datetime.date.today()
            total_amount_paid = 0

            # Update each pending installment
            for installment in pending_installments:
                # Update installment status
                installment.installment_state = "Pagada"
                installment.payment_date = today

                # Calculate amount
                amount = int(installment.installments_value)
                total_amount_paid += amount

                # Create reconciliation record directly
                reconciliation = Reconciliation(
                    payment_channel="Payment Gateway (Auto)",
                    payment_reference=payment_reference,
                    payment_amount=amount,
                    transaction_date=today,
                    observation=f"Auto payment - Installment {installment.installments_number} marked as paid via payment gateway",
                )
                session.add(reconciliation)

            # Check if all installments for this credit are now paid
            all_installments_query = select(Installment).where(
                Installment.credit_id == credit_id
            )
            all_installments_result = await session.execute(all_installments_query)
            all_installments = all_installments_result.scalars().all()

            all_paid = all(
                inst.installment_state == "Pagada" for inst in all_installments
            )

            # Update credit state if all installments are paid
            if all_paid:
                credit_query = select(Credit).where(Credit.id == credit_id)
                credit_result = await session.execute(credit_query)
                credit = credit_result.scalar_one_or_none()

                if credit and credit.credit_state != "Pagado":
                    credit.credit_state = "Pagado"

            # Commit all changes
            await session.commit()

        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to auto-process pending installments: {str(e)}",
            )
