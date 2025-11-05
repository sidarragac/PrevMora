from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ....config.database import get_db_session
from ....controllers.installment import InstallmentController
from ....schemas.base import PaginationParams
from ....schemas.Installment import (
    InstallmentCreate,
    InstallmentList,
    InstallmentResponse,
    InstallmentUpdate,
)

router = APIRouter()


@router.get(
    "/get_installment_by_id/{installment_id}",
    response_model=InstallmentResponse,
    tags=["Installments"],
)
async def get_installment_by_id(
    installment_id: int, session: AsyncSession = Depends(get_db_session)
):
    controller = InstallmentController()
    return await controller.get_by_id(session, installment_id)


@router.post("/get_installments", response_model=InstallmentList, tags=["Installments"])
async def get_installments(
    pagination: PaginationParams, session: AsyncSession = Depends(get_db_session)
):
    controller = InstallmentController()
    return await controller.get_multi_paginated(session, pagination)


@router.post(
    "/create_installment", response_model=InstallmentResponse, tags=["Installments"]
)
async def create_installment(
    installment: InstallmentCreate, session: AsyncSession = Depends(get_db_session)
):
    controller = InstallmentController()
    return await controller.create(session, installment)


@router.patch(
    "/update_installment/{installment_id}",
    response_model=InstallmentResponse,
    tags=["Installments"],
)
async def update_installment(
    installment_id: int,
    installment: InstallmentUpdate,
    session: AsyncSession = Depends(get_db_session),
):
    controller = InstallmentController()
    return await controller.update(session, installment_id, installment)
