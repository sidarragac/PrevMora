from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from ....config.database import get_db_session
from ....schemas.base import PaginationParams
from ....controllers.client import ClientController
from ....schemas.Client import ClientResponse, ClientCreate, ClientUpdate, ClientList

router = APIRouter()

@router.get("/get_client_by_id/{client_id}", response_model=ClientResponse, tags=["Clients"])
async def get_client_by_id(client_id: int, session: AsyncSession = Depends(get_db_session)):
    controller = ClientController()
    return await controller.get_by_id(session, client_id)

@router.post("/get_clients", response_model=ClientList, tags=["Clients"])
async def get_clients(pagination: PaginationParams, session: AsyncSession = Depends(get_db_session)):
    controller = ClientController()
    return await controller.get_multi_paginated(session, pagination)

@router.post("/create_client", response_model=ClientResponse, tags=["Clients"])
async def create_client(client: ClientCreate, session: AsyncSession = Depends(get_db_session)):
    controller = ClientController()
    return await controller.create(session, client)

@router.patch("/update_client/{client_id}", response_model=ClientResponse, tags=["Clients"])
async def update_client(client_id: int, client_update: ClientUpdate, session: AsyncSession = Depends(get_db_session)):
    controller = ClientController()
    return await controller.update(session, client_id, client_update)

