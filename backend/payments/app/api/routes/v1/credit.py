from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ....config.database import get_db_session
from ....controllers.credit import CreditController
from ....schemas.base import PaginationParams
from ....schemas.Credit import CreditCreate, CreditList, CreditResponse, CreditUpdate

router = APIRouter()


@router.get(
    "/get_credit_by_id/{credit_id}", response_model=CreditResponse, tags=["Credits"]
)
async def get_credit_by_id(
    credit_id: int, session: AsyncSession = Depends(get_db_session)
):
    controller = CreditController()
    return await controller.get_by_id(session, credit_id)


@router.post("/get_credits", response_model=CreditList, tags=["Credits"])
async def get_credits(
    pagination: PaginationParams, session: AsyncSession = Depends(get_db_session)
):
    controller = CreditController()
    return await controller.get_multi_paginated(session, pagination)


@router.post("/create_credit", response_model=CreditResponse, tags=["Credits"])
async def create_credit(
    credit: CreditCreate, session: AsyncSession = Depends(get_db_session)
):
    controller = CreditController()
    return await controller.create(session, credit)


@router.patch(
    "/update_credit/{credit_id}", response_model=CreditResponse, tags=["Credits"]
)
async def update_credit(
    credit_id: int,
    credit: CreditUpdate,
    session: AsyncSession = Depends(get_db_session),
):
    controller = CreditController()
    return await controller.update(session, credit_id, credit)
