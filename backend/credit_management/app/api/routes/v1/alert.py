from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from ....config.database import get_db_session
from ....schemas.base import PaginationParams
from ....controllers.alert import AlertController
from ....schemas.Alert import AlertCreate, AlertResponse, AlertList

router = APIRouter()

@router.get("/get_alert_by_id/{alert_id}", response_model=AlertResponse, tags=["Alerts"])
async def get_alert_by_id(alert_id: int, session: AsyncSession = Depends(get_db_session)):
    controller = AlertController()
    return await controller.get_by_id(session, alert_id)

@router.post("/get_alerts", response_model=AlertList, tags=["Alerts"])
async def get_alerts(pagination: PaginationParams, session: AsyncSession = Depends(get_db_session)):
    controller = AlertController()
    return await controller.get_multi_paginated(session, pagination)

@router.post("/create_alert", response_model=AlertResponse, tags=["Alerts"])
async def create_alert(alert: AlertCreate, session: AsyncSession = Depends(get_db_session)):
    controller = AlertController()
    return await controller.create(session, alert)

