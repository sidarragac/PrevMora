from app.config.database import get_db_session
from app.config.settings import settings
from app.controllers.analytics import (
    MONTHS,
    average_recovery_for_selected_months,
    calculate_money_recovery_by_month,
)
from app.schemas.analytics import MesSeleccion
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/health")
async def health():
    return {"service": settings.APP_NAME, "status": "ok"}


@router.get("/money-recovery-month")
async def money_recovery(db: AsyncSession = Depends(get_db_session)):
    return await calculate_money_recovery_by_month(db)


@router.post("/promedio-recuperacion-por-mes")
async def promedio_recuperacion_por_mes(
    seleccion: MesSeleccion, db: AsyncSession = Depends(get_db_session)
):
    meses_seleccionados = [mes for mes in MONTHS if getattr(seleccion, mes) is True]
    if not meses_seleccionados:
        return {
            "mensaje": "No has seleccionado ningún mes",
            "seleccion": [],
            "promedio_recuperacion": 0,
        }
    return await average_recovery_for_selected_months(meses_seleccionados, db)
