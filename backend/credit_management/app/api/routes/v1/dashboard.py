"""
Dashboard API routes
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ....config.database import get_db_session
from ....controllers.alert import AlertController
from ....controllers.client import ClientController
from ....controllers.credit import CreditController
from ....controllers.installment import InstallmentController
from ....controllers.manager import ManagerController
from ....controllers.portfolio import PortfolioController
from ....controllers.reconciliation import ReconciliationController
from ....schemas.base import PaginationParams
from ....schemas.Dashboard import DashboardData, DashboardStats

router = APIRouter()


@router.post("/get_dashboard_data", response_model=DashboardData, tags=["Dashboard"])
async def get_dashboard_data(
    pagination: PaginationParams, session: AsyncSession = Depends(get_db_session)
):
    """
    Get consolidated dashboard data in a single request.
    
    This endpoint replaces 7 separate API calls with one, retrieving:
    - Total counts for all entities (clients, credits, alerts, etc.)
    - Recent alerts
    - Recent installments
    - Recent portfolio managements
    - Recent reconciliations
    
    Args:
        pagination: Pagination parameters for recent items
        session: Database session
        
    Returns:
        DashboardData: Consolidated dashboard information
    """
    # Initialize controllers
    client_controller = ClientController()
    credit_controller = CreditController()
    alert_controller = AlertController()
    installment_controller = InstallmentController()
    portfolio_controller = PortfolioController()
    reconciliation_controller = ReconciliationController()
    manager_controller = ManagerController()

    # Fetch all data
    clients_data = await client_controller.get_multi_paginated(session, pagination)
    credits_data = await credit_controller.get_multi_paginated(session, pagination)
    alerts_data = await alert_controller.get_multi_paginated(session, pagination)
    installments_data = await installment_controller.get_multi_paginated(
        session, pagination
    )
    portfolios_data = await portfolio_controller.get_multi_paginated(
        session, pagination
    )
    reconciliations_data = await reconciliation_controller.get_multi_paginated(
        session, pagination
    )
    managers_data = await manager_controller.get_multi_paginated(session, pagination)

    # Build stats
    stats = DashboardStats(
        total_clients=clients_data.total,
        total_credits=credits_data.total,
        total_alerts=alerts_data.total,
        total_installments=installments_data.total,
        total_portfolio_managements=portfolios_data.total,
        total_reconciliations=reconciliations_data.total,
        total_managers=managers_data.total,
    )

    # Build dashboard data
    dashboard_data = DashboardData(
        stats=stats,
        recent_alerts=alerts_data.items,
        recent_installments=installments_data.items,
        recent_portfolio_managements=portfolios_data.items,
        recent_reconciliations=reconciliations_data.items,
    )

    return dashboard_data
