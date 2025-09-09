from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession


from ....config.database import get_db_session

from ....schemas.Client import ClientResponse
from ....repository.base import BaseRepository

# Client model and schemas
from ....models.Client import Client
from ....schemas.Client import ClientResponse, ClientCreate, ClientUpdate

# Alert model and schemas
from ....models.Alert import Alert
from ....schemas.Alert import AlertCreate, AlertResponse

# Credit model and schemas
from ....models.Credit import Credit
from ....schemas.Credit import CreditResponse, CreditCreate, CreditUpdate

router = APIRouter()

# Client Endpoints
@router.get("/get_client_by_id/{client_id}", response_model=ClientResponse)
async def get_client_by_id(client_id: int, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Client, get_schema=ClientResponse)
    client = await repository.get_by_id(session, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

# Alert Endpoints
@router.get("/get_alert_by_id/{alert_id}", response_model=AlertResponse)
async def get_alert_by_id(alert_id: int, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Alert, get_schema=AlertResponse)
    alert = await repository.get_by_id(session, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


# Credit Endpoints
@router.get("/get_credit_by_id/{credit_id}", response_model=CreditResponse)
async def get_credit_by_id(credit_id: int, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(model=Credit, get_schema=CreditResponse)
    credit = await repository.get_by_id(session, credit_id)
    if not credit:
        raise HTTPException(status_code=404, detail="Credit not found")
    return credit