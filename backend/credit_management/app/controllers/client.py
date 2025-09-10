from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.Alert import Alert
from ..models.Client import Client
from ..models.Credit import Credit
from ..models.Installment import Installment
from ..models.Portfolio import Portfolio
from ..models.Reconciliation import Reconciliation
from ..schemas.Client import (
    AlertDetailResponse,
    ClientCompleteResponse,
    ClientCreate,
    ClientList,
    ClientResponse,
    ClientUpdate,
    CreditDetailResponse,
    InstallmentDetailResponse,
    PortfolioDetailResponse,
    ReconciliationDetailResponse,
)
from .base import BaseController


class ClientController(BaseController):
    """Controller for Client operations."""

    def __init__(self):
        super().__init__(
            model=Client,
            get_schema=ClientResponse,
            create_schema=ClientCreate,
            update_schema=ClientUpdate,
            list_schema=ClientList,
            not_found_message="Client not found",
        )

    async def get_client_complete_data(
        self, session: AsyncSession, client_id: int
    ) -> ClientCompleteResponse:
        """
        Get all data associated with a specific client including:
        - Client basic information
        - All credits
        - All installments for each credit
        - All portfolio managements for each installment
        - All alerts for the client
        - All reconciliations related to the client's credits
        """

        # Traer el cliente con todas sus relaciones
        query = (
            select(Client)
            .where(Client.id == client_id)
            .options(
                selectinload(Client.credit)
                .selectinload(Credit.installment)
                .selectinload(Installment.portfolio),
                selectinload(Client.alert),
            )
        )

        result = await session.execute(query)
        client = result.scalar_one_or_none()

        if not client:
            raise HTTPException(status_code=404, detail=self.not_found_message)

        # Construir los créditos con sus cuotas y gestiones
        credits_data = []
        total_installments = 0
        total_portfolio_managements = 0
        payment_references = []

        for credit in client.credit:
            payment_references.append(credit.payment_reference)

            installments_data = []
            for installment in credit.installment:
                total_installments += 1

                portfolio_data = []
                for portfolio in installment.portfolio:
                    total_portfolio_managements += 1
                    portfolio_data.append(
                        PortfolioDetailResponse.model_validate(portfolio)
                    )

                installment_response = InstallmentDetailResponse.model_validate(
                    installment
                )
                installment_response.portfolio = portfolio_data
                installments_data.append(installment_response)

            credit_response = CreditDetailResponse.model_validate(credit)
            credit_response.installments = installments_data
            credits_data.append(credit_response)

        # Traer alertas del cliente
        alerts_data = [
            AlertDetailResponse.model_validate(alert) for alert in client.alert
        ]

        # Traer reconciliaciones relacionadas con los payment_references del cliente
        reconciliations_data = []
        if payment_references:
            reconciliation_query = select(Reconciliation).where(
                Reconciliation.payment_reference.in_(payment_references)
            )
            reconciliation_result = await session.execute(reconciliation_query)
            reconciliations = reconciliation_result.scalars().all()
            reconciliations_data = [
                ReconciliationDetailResponse.model_validate(rec)
                for rec in reconciliations
            ]

        # Construir la respuesta completa
        client_response = ClientCompleteResponse.model_validate(client)
        client_response.credits = credits_data
        client_response.alerts = alerts_data
        client_response.reconciliations = reconciliations_data

        # Agregar estadísticas
        client_response.total_credits = len(credits_data)
        client_response.total_installments = total_installments
        client_response.total_portfolio_managements = total_portfolio_managements
        client_response.total_alerts = len(alerts_data)
        client_response.total_reconciliations = len(reconciliations_data)

        return client_response
