"""
API Routes for all entities
"""
from fastapi import APIRouter

from .client import router as client_router
from .alert import router as alert_router
from .credit import router as credit_router
from .manager import router as manager_router
from .portfolio import router as portfolio_router
from .installment import router as installment_router
from .reconciliation import router as reconciliation_router

# Combined router for all entity endpoints
entities_router = APIRouter()

# Include all entity routers
entities_router.include_router(client_router, prefix="/clients", tags=["Clients"])
entities_router.include_router(alert_router, prefix="/alerts", tags=["Alerts"])
entities_router.include_router(credit_router, prefix="/credits", tags=["Credits"])
entities_router.include_router(manager_router, prefix="/managers", tags=["Managers"])
entities_router.include_router(portfolio_router, prefix="/portfolios", tags=["Portfolios"])
entities_router.include_router(installment_router, prefix="/installments", tags=["Installments"])
entities_router.include_router(reconciliation_router, prefix="/reconciliations", tags=["Reconciliations"])

