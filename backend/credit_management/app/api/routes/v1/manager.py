from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ....config.database import get_db_session
from ....controllers.manager import ManagerController
from ....schemas.base import PaginationParams
from ....schemas.Manager import (
    ManagerCreate,
    ManagerList,
    ManagerResponse,
    ManagerUpdate,
)

router = APIRouter()


@router.get(
    "/get_manager_by_id/{manager_id}", response_model=ManagerResponse, tags=["Managers"]
)
async def get_manager_by_id(
    manager_id: int, session: AsyncSession = Depends(get_db_session)
):
    controller = ManagerController()
    return await controller.get_by_id(session, manager_id)


@router.post("/get_managers", response_model=ManagerList, tags=["Managers"])
async def get_managers(
    pagination: PaginationParams, session: AsyncSession = Depends(get_db_session)
):
    controller = ManagerController()
    return await controller.get_multi_paginated(session, pagination)


@router.post("/create_manager", response_model=ManagerResponse, tags=["Managers"])
async def create_manager(
    manager: ManagerCreate, session: AsyncSession = Depends(get_db_session)
):
    controller = ManagerController()
    return await controller.create(session, manager)
