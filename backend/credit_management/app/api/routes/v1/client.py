from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ....config.database import get_db_session
from ....controllers.client import ClientController
from ....schemas.base import PaginationParams
from ....schemas.Client import (
    ClientCompleteResponse,
    ClientCreate,
    ClientList,
    ClientResponse,
    ClientUpdate,
    CreditCalculatedInstallmentResponse,
)

router = APIRouter()


@router.get(
    "/get_client_by_id/{client_id}", response_model=ClientResponse, tags=["Clients"]
)
async def get_client_by_id(
    client_id: int, session: AsyncSession = Depends(get_db_session)
):
    controller = ClientController()
    return await controller.get_by_id(session, client_id)


@router.post("/get_clients", response_model=ClientList, tags=["Clients"])
async def get_clients(
    pagination: PaginationParams, session: AsyncSession = Depends(get_db_session)
):
    controller = ClientController()
    return await controller.get_multi_paginated(session, pagination)


@router.post("/create_client", response_model=ClientResponse, tags=["Clients"])
async def create_client(
    client: ClientCreate, session: AsyncSession = Depends(get_db_session)
):
    controller = ClientController()
    return await controller.create(session, client)


@router.patch(
    "/update_client/{client_id}", response_model=ClientResponse, tags=["Clients"]
)
async def update_client(
    client_id: int,
    client_update: ClientUpdate,
    session: AsyncSession = Depends(get_db_session),
):
    controller = ClientController()
    return await controller.update(session, client_id, client_update)


@router.get(
    "/get_client_complete_data/{client_id}",
    response_model=ClientCompleteResponse,
    tags=["Clients"],
)
async def get_client_complete_data(
    client_id: int, session: AsyncSession = Depends(get_db_session)
):
    controller = ClientController()
    return await controller.get_client_complete_data(session, client_id)


@router.get(
    "/get_credits_detailed/{client_id}",
    response_model=List[CreditCalculatedInstallmentResponse],
    tags=["Clients"],
)
async def get_credits_detailed(
    client_id: int, session: AsyncSession = Depends(get_db_session)
):
    controller = ClientController()
    return await controller.get_credits_detailed(session, client_id)
