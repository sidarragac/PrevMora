from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db_session
from app.controllers.analytics import fetch_portfolio, contacts_by_manager


router = APIRouter()


@router.get("/portfolio")
async def get_portfolio(db: AsyncSession = Depends(get_db_session)):
    return await fetch_portfolio(db)


@router.get("/managers/contacts")
async def get_contacts_by_manager(db: AsyncSession = Depends(get_db_session)):
    return await contacts_by_manager(db)