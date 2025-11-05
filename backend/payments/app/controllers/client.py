from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.Alert import Alert
from ..models.Client import Client
from ..models.Credit import Credit
from ..models.Installment import Installment
from ..models.Manager import Manager
from ..models.Portfolio import Portfolio
from ..models.Reconciliation import Reconciliation
from ..schemas.Client import (
    AlertDetailResponse,
    ClientCompleteResponse,
    ClientCreate,
    ClientList,
    ClientResponse,
    ClientUpdate,
    CreditCalculatedInstallmentResponse,
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

        query = (
            select(Client)
            .where(Client.id == client_id)
            .options(
                selectinload(Client.credit)
                .selectinload(Credit.installment)
                .selectinload(Installment.portfolio)
                .selectinload(Portfolio.manager),
                selectinload(Client.alert),
            )
        )

        result = await session.execute(query)
        client = result.scalar_one_or_none()

        if not client:
            raise HTTPException(status_code=404, detail=self.not_found_message)

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
                    portfolio_response = PortfolioDetailResponse.model_validate(
                        portfolio
                    )
                    if portfolio.manager:
                        portfolio_response.manager_name = portfolio.manager.name
                    portfolio_data.append(portfolio_response)

                installment_response = InstallmentDetailResponse.model_validate(
                    installment
                )
                installment_response.portfolio = portfolio_data
                installments_data.append(installment_response)

            credit_response = CreditDetailResponse.model_validate(credit)
            credit_response.installments = installments_data
            credits_data.append(credit_response)

        alerts_data = [
            AlertDetailResponse.model_validate(alert) for alert in client.alert
        ]

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

        client_response = ClientCompleteResponse.model_validate(client)
        client_response.credits = credits_data
        client_response.alerts = alerts_data
        client_response.reconciliations = reconciliations_data

        client_response.total_credits = len(credits_data)
        client_response.total_installments = total_installments
        client_response.total_portfolio_managements = total_portfolio_managements
        client_response.total_alerts = len(alerts_data)
        client_response.total_reconciliations = len(reconciliations_data)

        return client_response

    async def get_credits_detailed(
        self, session: AsyncSession, client_id: int
    ) -> list[CreditCalculatedInstallmentResponse]:
        """
        Get detailed credit information for a specific client.
        """
        query = (
            select(Credit)
            .where(Credit.client_id == client_id)
            .options(
                selectinload(Credit.installment)
                .selectinload(Installment.portfolio)
                .selectinload(Portfolio.manager)
            )
        )

        result = await session.execute(query)
        credits = result.scalars().all()

        if not credits:
            raise HTTPException(
                status_code=404, detail="No credits found for the client"
            )

        credits_data = []

        for credit in credits:
            installments_data = []
            for installment in credit.installment:
                portfolio_data = []
                for portfolio in installment.portfolio:
                    portfolio_response = PortfolioDetailResponse.model_validate(
                        portfolio
                    )
                    if portfolio.manager:
                        portfolio_response.manager_name = portfolio.manager.name
                    portfolio_data.append(portfolio_response)

                installment_response = InstallmentDetailResponse.model_validate(
                    installment
                )
                installment_response.portfolio = portfolio_data
                installments_data.append(installment_response)

            credit_response = CreditCalculatedInstallmentResponse.model_validate(credit)
            credit_response.installments = installments_data
            credits_data.append(credit_response)

        for credit in credits:
            query_reconciliations = select(Reconciliation).where(
                Reconciliation.payment_reference == credit.payment_reference
            )
            result_reconciliations = await session.execute(query_reconciliations)

            sum_payments = sum(
                rec.payment_amount for rec in result_reconciliations.scalars().all()
            )

            for credit_data in credits_data:
                if credit_data.id == credit.id:
                    credit_data.total_paid = sum_payments
                    credit_data.total_pending = int(
                        credit_data.disbursement_amount - sum_payments
                    )
                    break

        return credits_data
