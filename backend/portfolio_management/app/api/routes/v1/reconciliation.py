from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ....config.database import get_db_session
from ....controllers.reconciliation import ReconciliationController
from ....schemas.base import PaginationParams
from ....schemas.Reconciliation import (
    ReconciliationCreate,
    ReconciliationList,
    ReconciliationResponse,
)

router = APIRouter()


@router.get(
    "/get_reconciliation_by_id/{reconciliation_id}",
    response_model=ReconciliationResponse,
    tags=["Reconciliations"],
)
async def get_reconciliation_by_id(
    reconciliation_id: int, session: AsyncSession = Depends(get_db_session)
):
    controller = ReconciliationController()
    return await controller.get_by_id(session, reconciliation_id)


@router.post(
    "/get_reconciliations", response_model=ReconciliationList, tags=["Reconciliations"]
)
async def get_reconciliations(
    pagination: PaginationParams, session: AsyncSession = Depends(get_db_session)
):
    controller = ReconciliationController()
    return await controller.get_multi_paginated(session, pagination)


@router.post(
    "/create_reconciliation",
    response_model=ReconciliationResponse,
    tags=["Reconciliations"],
)
async def create_reconciliation(
    reconciliation: ReconciliationCreate,
    session: AsyncSession = Depends(get_db_session),
):
    controller = ReconciliationController()
    return await controller.create(session, reconciliation)
