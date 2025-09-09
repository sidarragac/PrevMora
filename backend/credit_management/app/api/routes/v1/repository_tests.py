from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession


from ....config.database import get_db_session

from ....schemas.Client import ClientResponse
from ....repository.base import BaseRepository

# Client model and schemas
from ....models.Client import Client
from ....schemas.Client import ClientResponse, ClientCreate, ClientUpdate, ClientList

# Alert model and schemas
from ....models.Alert import Alert
from ....schemas.Alert import AlertCreate, AlertResponse, AlertList

# Credit model and schemas
from ....models.Credit import Credit
from ....schemas.Credit import CreditResponse, CreditCreate, CreditUpdate, CreditList

# Manager model and schemas
from ....models.Manager import Manager
from ....schemas.Manager import ManagerResponse, ManagerUpdate, ManagerCreate, ManagerList

# Portfolio model and schemas
from ....models.Portfolio import Portfolio
from ....schemas.Portfolio import PortfolioResponse, PortfolioCreate, PortfolioUpdate, PortfolioList

# Installment model and schemas
from ....models.Installment import Installment
from ....schemas.Installment import InstallmentResponse, InstallmentCreate, InstallmentList

# Reconciliation model and schemas
from ....models.Reconciliation import Reconciliation
from ....schemas.Reconciliation import ReconciliationResponse, ReconciliationCreate, ReconciliationList

from ....schemas.base import PaginationParams

router = APIRouter()

# Client Endpoints
@router.get("/get_client_by_id/{client_id}", response_model=ClientResponse, tags=["Clients"])
async def get_client_by_id(client_id: int, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Client, get_schema=ClientResponse)
    client = await repository.get_by_id(session, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.post("/get_clients", response_model=ClientList, tags=["Clients"])
async def get_clients(pagination: PaginationParams, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Client, get_schema=ClientResponse, list_schema=ClientList)
    clients = await repository.get_multi_paginated(session, pagination)
    return clients

@router.post("/create_client", response_model=ClientResponse, tags=["Clients"])
async def create_client(client: ClientCreate, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Client, get_schema=ClientResponse)
    new_client = await repository.create(session, client)
    return new_client

@router.patch("/update_client/{client_id}", response_model=ClientResponse, tags=["Clients"])
async def update_client(client_id: int, client_update: ClientUpdate, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Client, get_schema=ClientResponse)
    updated_client = await repository.update(session, client_id, client_update)
    if not updated_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated_client

# Alert Endpoints
@router.get("/get_alert_by_id/{alert_id}", response_model=AlertResponse, tags=["Alerts"])
async def get_alert_by_id(alert_id: int, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Alert, get_schema=AlertResponse)
    alert = await repository.get_by_id(session, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.post("/get_alerts", response_model=AlertList, tags=["Alerts"])
async def get_alerts(pagination: PaginationParams, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Alert, get_schema=AlertResponse, list_schema=AlertList)
    alerts = await repository.get_multi_paginated(session, pagination)
    return alerts

@router.post("/create_alert", response_model=AlertResponse, tags=["Alerts"])
async def create_alert(alert: AlertCreate, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Alert, get_schema=AlertResponse)
    new_alert = await repository.create(session, alert)
    return new_alert


# Credit Endpoints
@router.get("/get_credit_by_id/{credit_id}", response_model=CreditResponse, tags=["Credits"])
async def get_credit_by_id(credit_id: int, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Credit, get_schema=CreditResponse)
    credit = await repository.get_by_id(session, credit_id)
    if not credit:
        raise HTTPException(status_code=404, detail="Credit not found")
    return credit

@router.post("/get_credits", response_model=CreditList, tags=["Credits"])
async def get_credits(pagination: PaginationParams, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Credit, get_schema=CreditResponse, list_schema=CreditList)
    credits = await repository.get_multi_paginated(session, pagination)
    return credits

@router.post("/create_credit", response_model=CreditResponse, tags=["Credits"])
async def create_credit(credit: CreditCreate, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Credit, get_schema=CreditResponse)
    new_credit = await repository.create(session, credit)
    return new_credit

# Manager Endpoints
@router.get("/get_manager_by_id/{manager_id}", response_model=ManagerResponse, tags=["Managers"])
async def get_manager_by_id(manager_id: int, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Manager, get_schema=ManagerResponse)
    manager = await repository.get_by_id(session, manager_id)
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    return manager

@router.post("/get_managers", response_model=ManagerList, tags=["Managers"])
async def get_managers(pagination: PaginationParams, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Manager, get_schema=ManagerResponse, list_schema=ManagerList)
    managers = await repository.get_multi_paginated(session, pagination)
    return managers

@router.post("/create_manager", response_model=ManagerResponse, tags=["Managers"])
async def create_manager(manager: ManagerCreate, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Manager, get_schema=ManagerResponse)
    new_manager = await repository.create(session, manager)
    return new_manager

# Portfolio Endpoints
@router.get("/get_portfolio_by_id/{portfolio_id}", response_model=PortfolioResponse, tags=["Portfolios"])
async def get_portfolio_by_id(portfolio_id: int, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Portfolio, get_schema=PortfolioResponse)
    portfolio = await repository.get_by_id(session, portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio

@router.post("/get_portfolios", response_model=PortfolioList, tags=["Portfolios"])
async def get_portfolios(pagination: PaginationParams, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Portfolio, get_schema=PortfolioResponse, list_schema=PortfolioList)
    portfolios = await repository.get_multi_paginated(session, pagination)
    return portfolios

@router.post("/create_portfolio", response_model=PortfolioResponse, tags=["Portfolios"])
async def create_portfolio(portfolio: PortfolioCreate, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Portfolio, get_schema=PortfolioResponse)
    new_portfolio = await repository.create(session, portfolio)
    return new_portfolio

# Installment Endpoints
@router.get("/get_installment_by_id/{installment_id}", response_model=InstallmentResponse, tags=["Installments"])
async def get_installment_by_id(installment_id: int, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Installment, get_schema=InstallmentResponse)
    installment = await repository.get_by_id(session, installment_id)
    if not installment:
        raise HTTPException(status_code=404, detail="Installment not found")
    return installment

@router.post("/get_installments", response_model=InstallmentList, tags=["Installments"])
async def get_installments(pagination: PaginationParams, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Installment, get_schema=InstallmentResponse, list_schema=InstallmentList)
    installments = await repository.get_multi_paginated(session, pagination)
    return installments

@router.post("/create_installment", response_model=InstallmentResponse, tags=["Installments"])
async def create_installment(installment: InstallmentCreate, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Installment, get_schema=InstallmentResponse)
    new_installment = await repository.create(session, installment)
    return new_installment

# Reconciliation Endpoints
@router.get("/get_reconciliation_by_id/{reconciliation_id}", response_model=ReconciliationResponse, tags=["Reconciliations"])
async def get_reconciliation_by_id(reconciliation_id: int, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Reconciliation, get_schema=ReconciliationResponse)
    reconciliation = await repository.get_by_id(session, reconciliation_id)
    if not reconciliation:
        raise HTTPException(status_code=404, detail="Reconciliation not found")
    return reconciliation

@router.post("/get_reconciliations", response_model=ReconciliationList, tags=["Reconciliations"])
async def get_reconciliations(pagination: PaginationParams, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Reconciliation, get_schema=ReconciliationResponse, list_schema=ReconciliationList)
    reconciliations = await repository.get_multi_paginated(session, pagination)
    return reconciliations

@router.post("/create_reconciliation", response_model=ReconciliationResponse, tags=["Reconciliations"])
async def create_reconciliation(reconciliation: ReconciliationCreate, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Reconciliation, get_schema=ReconciliationResponse)
    new_reconciliation = await repository.create(session, reconciliation)
    return new_reconciliation