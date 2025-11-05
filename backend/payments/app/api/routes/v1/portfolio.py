from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ....config.database import get_db_session
from ....controllers.portfolio import PortfolioController
from ....schemas.base import PaginationParams
from ....schemas.Portfolio import (
    PortfolioCreate,
    PortfolioList,
    PortfolioResponse,
    PortfolioUpdate,
)

router = APIRouter()


@router.get(
    "/get_portfolio_by_id/{portfolio_id}",
    response_model=PortfolioResponse,
    tags=["Portfolios"],
)
async def get_portfolio_by_id(
    portfolio_id: int, session: AsyncSession = Depends(get_db_session)
):
    controller = PortfolioController()
    return await controller.get_by_id(session, portfolio_id)


@router.post("/get_portfolios", response_model=PortfolioList, tags=["Portfolios"])
async def get_portfolios(
    pagination: PaginationParams, session: AsyncSession = Depends(get_db_session)
):
    controller = PortfolioController()
    return await controller.get_multi_paginated(session, pagination)


@router.post("/create_portfolio", response_model=PortfolioResponse, tags=["Portfolios"])
async def create_portfolio(
    portfolio: PortfolioCreate, session: AsyncSession = Depends(get_db_session)
):
    controller = PortfolioController()
    return await controller.create(session, portfolio)


@router.patch(
    "/update_portfolio/{portfolio_id}",
    response_model=PortfolioResponse,
    tags=["Portfolios"],
)
async def update_portfolio(
    portfolio_id: int,
    portfolio: PortfolioUpdate,
    session: AsyncSession = Depends(get_db_session),
):
    controller = PortfolioController()
    return await controller.update(session, portfolio_id, portfolio)
