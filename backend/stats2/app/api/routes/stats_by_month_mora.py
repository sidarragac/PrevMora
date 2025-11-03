from fastapi import APIRouter, Depends
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from app.config.settings import settings
from app.config.database import get_db_session
from app.models.client import Client
from app.models.credit import Credit
from app.models.installment import Installment
import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.get("/health")
async def health():
    return {"service": settings.APP_NAME, "status": "ok"}
    
@router.get("/installments/by-month")
async def installments_by_month(db: AsyncSession = Depends(get_db_session)):
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
    
    # Overdue installments grouped by month
    overdue_query = select(
        Installment.id,
        Installment.credit_id,
        Installment.installments_number,
        Installment.due_date,
        Installment.installments_value,
        Installment.installment_state,
        Installment.payment_date,
    ).where(Installment.installment_state == "Vencida")

    overdue_result = await db.execute(overdue_query)
    overdue_rows = overdue_result.fetchall()

    overdue_grouped = {}
    for month_name in month_names.values():
        overdue_grouped[month_name] = []

    for row in overdue_rows:
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
            overdue_grouped[month_name].append(item)

    Porcentaje_Morosidad=[]
    Comparacion_Mes_Anterior=[]
    for month in month_names.values():
        if len(grouped[month])==0 or len(overdue_grouped[month])==0:
            Porcentaje_Morosidad.append("0")
        else:
            Porcentaje_Morosidad.append(f"{(len(overdue_grouped[month])/len(grouped[month]))*100}")
        
    for i in range(len(Porcentaje_Morosidad)):
            if i==0:    
                Comparacion_Mes_Anterior.append("0")
            else:
                Comparacion_Mes_Anterior.append(f"{(float(Porcentaje_Morosidad[i])-float(Porcentaje_Morosidad[i-1]))}")
   
       

    datos=[f"Total de cuotas en Enero: {len(grouped['Enero'])}, Numero de cuotas Vencidas: {len(overdue_grouped['Enero'])},Porcentaje  Morosidad: {Porcentaje_Morosidad[0]}%, comparacion con el mes anterior: {Comparacion_Mes_Anterior[0]}",
    f"Total de cuotas en Febrero: {len(grouped['Febrero'])}, Numero de cuotas Vencidas: {len(overdue_grouped['Febrero'])},Porcentaje  Morosidad: {Porcentaje_Morosidad[1]}% comparacion con el mes anterior: {Comparacion_Mes_Anterior[1]}",
    f"Total de cuotas en Marzo: {len(grouped['Marzo'])}, Numero de cuotas Vencidas: {len(overdue_grouped['Marzo'])},Porcentaje de cuotas Morosidad: {Porcentaje_Morosidad[2]}% comparacion con el mes anterior: {Comparacion_Mes_Anterior[2]}",
    f"Total de cuotas en Abril: {len(grouped['Abril'])}, Numero de cuotas Vencidas: {len(overdue_grouped['Abril'])},Porcentaje  Morosidad: {Porcentaje_Morosidad[3]}% comparacion con el mes anterior: {Comparacion_Mes_Anterior[3]}",
    f"Total de cuotas en Mayo: {len(grouped['Mayo'])}, Numero de cuotas Vencidas: {len(overdue_grouped['Mayo'])},Porcentaje  Morosidad: {Porcentaje_Morosidad[4]}% comparacion con el mes anterior: {Comparacion_Mes_Anterior[4]}",
    f"Total de cuotas en Junio: {len(grouped['Junio'])}, Numero de cuotas Vencidas: {len(overdue_grouped['Junio'])},Porcentaje  Morosidad: {Porcentaje_Morosidad[5]}% comparacion con el mes anterior: {Comparacion_Mes_Anterior[5]}",
    f"Total de cuotas en Julio: {len(grouped['Julio'])}, Numero de cuotas Vencidas: {len(overdue_grouped['Julio'])},Porcentaje de cuotas Morosidad: {Porcentaje_Morosidad[6]}% comparacion con el mes anterior: {Comparacion_Mes_Anterior[6]}",
    f"Total de cuotas en Agosto: {len(grouped['Agosto'])}, Numero de cuotas Vencidas: {len(overdue_grouped['Agosto'])},Porcentaje de cuotas Morosidad: {Porcentaje_Morosidad[7]}% comparacion con el mes anterior: {Comparacion_Mes_Anterior[7]}",
    f"Total de cuotas en Septiembre: {len(grouped['Septiembre'])}, Numero de cuotas Vencidas: {len(overdue_grouped['Septiembre'])},Porcentaje de cuotas Morosidad: {Porcentaje_Morosidad[8]}% comparacion con el mes anterior: {Comparacion_Mes_Anterior[8]}",
    f"Total de cuotas en Octubre: {len(grouped['Octubre'])}, Numero de cuotas Vencidas: {len(overdue_grouped['Octubre'])},Porcentaje de cuotas Morosidad: {Porcentaje_Morosidad[9]}% comparacion con el mes anterior: {Comparacion_Mes_Anterior[9]}",
    f"Total de cuotas en Noviembre: {len(grouped['Noviembre'])}, Numero de cuotas Vencidas: {len(overdue_grouped['Noviembre'])},Porcentaje de cuotas Morosidad: {Porcentaje_Morosidad[10]}% comparacion con el mes anterior: {Comparacion_Mes_Anterior[10]}",
    f"Total de cuotas en Diciembre: {len(grouped['Diciembre'])}, Numero de cuotas Vencidas: {len(overdue_grouped['Diciembre'])},Porcentaje de cuotas Morosidad: {Porcentaje_Morosidad[11]}% comparacion con el mes anterior: {Comparacion_Mes_Anterior[11]}"]
    
    DeudaPorMes=[0,0,0,0,0,0,0,0,0,0,0,0]
    MontoPorMes=[0,0,0,0,0,0,0,0,0,0,0,0]
    BalancePorMes=[0,0,0,0,0,0,0,0,0,0,0,0]
    
    Meses=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    
    for i in range(len(grouped)):
            for j in range(len(grouped[Meses[i]])):
                if grouped[Meses[i]][j]['installment_state']=="Pagada":
                    MontoPorMes[i]=MontoPorMes[i]+float(grouped[Meses[i]][j]['installments_value'])  
                if grouped[Meses[i]][j]['installment_state']=="Vencida":
                    DeudaPorMes[i]=DeudaPorMes[i]+float(grouped[Meses[i]][j]['installments_value'])
    for i in range(len(MontoPorMes)):
        BalancePorMes[i]=MontoPorMes[i]-DeudaPorMes[i]
    logging.info(f"Deuda por mes: {DeudaPorMes}")
    logging.info(f"Monto por mes: {MontoPorMes}")
    logging.info(f"Balance por mes: {BalancePorMes}")
    
        

    return {"installments": grouped, "datos": datos, "DeudaPorMes": DeudaPorMes, "MontoPorMes": MontoPorMes, "BalancePorMes": BalancePorMes}

