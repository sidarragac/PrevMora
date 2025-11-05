"""
Dashboard schemas for consolidated data retrieval
"""

from typing import Any, List

from pydantic import BaseModel

from .Alert import AlertResponse
from .Client import ClientResponse
from .Credit import CreditResponse
from .Installment import InstallmentResponse
from .Manager import ManagerResponse
from .Portfolio import PortfolioResponse
from .Reconciliation import ReconciliationResponse


class DashboardStats(BaseModel):
    """Statistics for the dashboard"""

    total_clients: int
    total_credits: int
    total_alerts: int
    total_installments: int
    total_portfolio_managements: int
    total_reconciliations: int
    total_managers: int


class DashboardData(BaseModel):
    """Complete dashboard data response"""

    stats: DashboardStats
    recent_alerts: List[AlertResponse]
    recent_installments: List[InstallmentResponse]
    recent_portfolio_managements: List[PortfolioResponse]
    recent_reconciliations: List[ReconciliationResponse]

    class Config:
        orm_mode = True
