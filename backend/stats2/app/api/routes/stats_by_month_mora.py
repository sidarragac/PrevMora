from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.config.database import get_db_session
from app.controllers.analytics import calculate_installments_by_month


router = APIRouter()


@router.get("/health")
async def health():
    return {"service": settings.APP_NAME, "status": "ok"}


@router.get("/installments/by-month")
async def installments_by_month(db: AsyncSession = Depends(get_db_session)):
    return await calculate_installments_by_month(db)

