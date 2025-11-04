from fastapi import APIRouter, Depends
from sqlalchemy import select, func, and_,or_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from app.config.settings import settings
from app.config.database import get_db_session
from app.models.client import Client
from app.models.credit import Credit
from app.models.installment import Installment
import logging
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)

router = APIRouter()

# Lista de meses en orden para reutilizar en endpoints
MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

@router.get("/health")
async def health():
    return {"service": settings.APP_NAME, "status": "ok"}

@router.get("/money-recovery-month")
async def money_recovery(db: AsyncSession = Depends(get_db_session)):
    return await calcular_recuperacion_por_mes(db)
 
async def calcular_recuperacion_por_mes(db: AsyncSession):
    query = select(
        Installment.id,
        Installment.credit_id,
        Installment.installments_number,
        Installment.due_date,
        Installment.installments_value,
        Installment.installment_state,
        Installment.payment_date,
    )

    result = await db.execute(query)
    rows = result.fetchall()

    month_names = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre",
    }
    grouped= {}
    for month_name in month_names.values():
        grouped[month_name] = []

    for row in rows:
        (
            id_,
            credit_id,
            installments_number,
            due_date,
            installments_value,
            installment_state,
            payment_date,
        ) = row

        month_name = month_names[due_date.month] if due_date else None
        item = {
            "id": id_,
            "credit_id": credit_id,
            "installments_number": installments_number,
            "due_date": due_date.strftime("%Y-%m-%d") if due_date else None,
            "installments_value": float(installments_value),
            "installment_state": installment_state,
            "payment_date": payment_date.strftime("%Y-%m-%d") if payment_date else None,
        }
        if month_name:
            grouped[month_name].append(item)
        
    
    
    Meses=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    RecuperacionPorMes=[0,0,0,0,0,0,0,0,0,0,0,0]
    PorcentajeRecuperacionPorMes=[0,0,0,0,0,0,0,0,0,0,0,0]
    DeudaTotalPorMes=[0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(len(grouped)):
            for j in range(len(grouped[Meses[i]])):
                if grouped[Meses[i]][j]['payment_date'] is not None:
                    if grouped[Meses[i]][j]['payment_date']>grouped[Meses[i]][j]['due_date']:
                        RecuperacionPorMes[i]=RecuperacionPorMes[i]+float(grouped[Meses[i]][j]['installments_value'])
                        DeudaTotalPorMes[i]=DeudaTotalPorMes[i]+float(grouped[Meses[i]][j]['installments_value'])
                if grouped[Meses[i]][j]['installment_state']=="Vencida":
                    DeudaTotalPorMes[i]=DeudaTotalPorMes[i]+float(grouped[Meses[i]][j]['installments_value'])


    for i in range(len(RecuperacionPorMes)):
        if RecuperacionPorMes[i]==0:
            PorcentajeRecuperacionPorMes[i]=0
        else:
          PorcentajeRecuperacionPorMes[i]=RecuperacionPorMes[i]/DeudaTotalPorMes[i]*100

    
    return {"RecuperacionPorMes": RecuperacionPorMes,  "DeudaTotalPorMes": DeudaTotalPorMes,"PorcentajeRecuperacionPorMes": PorcentajeRecuperacionPorMes}

class MesSeleccion(BaseModel):
    Enero: bool = False
    Febrero: bool = False
    Marzo: bool = False
    Abril: bool = False
    Mayo: bool = False
    Junio: bool = False
    Julio: bool = False
    Agosto: bool = False
    Septiembre: bool = False
    Octubre: bool = False
    Noviembre: bool = False
    Diciembre: bool = False

@router.post("/promedio-recuperacion-por-mes")
async def promedio_recuperacion_por_mes(seleccion: MesSeleccion, db: AsyncSession = Depends(get_db_session)):
    """
    Selecciona meses con checkboxes en Swagger y calcula el promedio de recuperación.
    """
    meses_seleccionados = []
    for mes in MESES:
        if getattr(seleccion, mes) == True:
            meses_seleccionados.append(mes)

    if not meses_seleccionados:
        return {"mensaje": "No has seleccionado ningún mes", "seleccion": [], "promedio_recuperacion": 0}

    datos = await calcular_recuperacion_por_mes(db)
    logging.info(f"Datos: {datos}")
    recuperacion = datos["RecuperacionPorMes"]
    indices = [MESES.index(mes) for mes in meses_seleccionados]
    valores = [recuperacion[i] for i in indices]
    promedio = sum(valores) / len(valores) if valores else 0

    return {"seleccion": meses_seleccionados, "valores": valores, "promedio_recuperacion": promedio}