import pathlib
import sys
from datetime import datetime, timedelta
from enum import Enum

from fastapi import APIRouter, Depends, Query
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


class MonthEnum(str, Enum):
    Enero = "Enero"
    Febrero = "Febrero"
    Marzo = "Marzo"
    Abril = "Abril"
    Mayo = "Mayo"
    Junio = "Junio"
    Julio = "Julio"
    Agosto = "Agosto"
    Septiembre = "Septiembre"
    Octubre = "Octubre"
    Noviembre = "Noviembre"
    Diciembre = "Diciembre"


# Add notifications app path to import its models and DB session
_BACKEND_DIR = pathlib.Path(__file__).resolve().parents[3]
_NOTIFICATIONS_APP_DIR = _BACKEND_DIR / "notifications" / "app"
if str(_NOTIFICATIONS_APP_DIR) not in sys.path:
    sys.path.append(str(_NOTIFICATIONS_APP_DIR))

from config.database import get_db_session  # type: ignore  # noqa: E402
from models.alert import Alert  # type: ignore  # noqa: E402
from models.client import Client  # type: ignore  # noqa: E402
from models.credit import Credit  # type: ignore  # noqa: E402
from models.installment import Installment  # type: ignore  # noqa: E402


@router.get("/client-alerts")
async def get_client_alerts(db: AsyncSession = Depends(get_db_session)):
    subquery = (
        select(
            Alert.client_id,
            Alert.credit_id,
            func.max(Installment.id).label("latest_installment_id"),
        )
        .select_from(Alert)
        .join(Installment, Alert.credit_id == Installment.credit_id)
        .group_by(Alert.client_id, Alert.credit_id)
    ).subquery()

    current_date = datetime.now().date()
    ten_days_future = current_date + timedelta(days=16)

    query = (
        select(
            Client.phone,
            Client.name,
            Installment.installments_value,
            Installment.due_date,
        )
        .select_from(subquery)
        .join(Client, subquery.c.client_id == Client.id)
        .join(Installment, subquery.c.latest_installment_id == Installment.id)
        .where(
            and_(
                Installment.due_date >= current_date,
                Installment.due_date <= ten_days_future,
            )
        )
    )

    result = await db.execute(query)
    rows = result.fetchall()

    recipients = []
    for row in rows:
        phone, name, amount, due_date = row

        formatted_amount = float(amount)
        formatted_date = due_date.strftime("%Y-%m-%d") if due_date else None

        recipients.append(
            {
                "to": "+" + phone,
                "name": name,
                "amount": formatted_amount,
                "date": formatted_date,
            }
        )

    response = {
        "phone_number": "default",
        "language": "Spanish (MEX)",
        "recipients": recipients,
    }

    return response


@router.get("/overdue-installments")
async def get_overdue_installments(
    db: AsyncSession = Depends(get_db_session),
    month_ref: MonthEnum = Query(
        default=MonthEnum.Enero, description="Mes de referencia"
    ),
    month_cmp: MonthEnum = Query(
        default=MonthEnum.Febrero, description="Mes a comparar"
    ),
):
    query = select(
        Installment.id,
        Installment.credit_id,
        Installment.installments_number,
        Installment.due_date,
        Installment.installments_value,
        Installment.installment_state,
        Installment.payment_date,
    ).where(Installment.installment_state == "Vencida")

    result = await db.execute(query)
    rows = result.fetchall()
    print(rows)

    installments = []
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

        installments.append(
            {
                "id": id_,
                "credit_id": credit_id,
                "installments_number": installments_number,
                "due_date": due_date.strftime("%Y-%m-%d") if due_date else None,
                "installments_value": float(installments_value),
                "installment_state": installment_state,
                "payment_date": (
                    payment_date.strftime("%Y-%m-%d") if payment_date else None
                ),
            }
        )
        cantidad_cuotas_vencidas_mes = {
            "Enero": [0, 0],
            "Febrero": [0, 0],
            "Marzo": [0, 0],
            "Abril": [0, 0],
            "Mayo": [0, 0],
            "Junio": [0, 0],
            "Julio": [0, 0],
            "Agosto": [0, 0],
            "Septiembre": [0, 0],
            "Octubre": [0, 0],
            "Noviembre": [0, 0],
            "Diciembre": [0, 0],
        }

        for installment in installments:
            due_date = installment["due_date"]
            if due_date:
                month = due_date.split("-")[1]
                if month == "01":
                    month = "Enero"
                elif month == "02":
                    month = "Febrero"
                elif month == "03":
                    month = "Marzo"
                elif month == "04":
                    month = "Abril"
                elif month == "05":
                    month = "Mayo"
                elif month == "06":
                    month = "Junio"
                elif month == "07":
                    month = "Julio"
                elif month == "08":
                    month = "Agosto"
                elif month == "09":
                    month = "Septiembre"
                elif month == "10":
                    month = "Octubre"
                elif month == "11":
                    month = "Noviembre"
                elif month == "12":
                    month = "Diciembre"
                cantidad_cuotas_vencidas_mes[month][0] = (
                    cantidad_cuotas_vencidas_mes[month][0]
                    + installment["installments_value"]
                )
                cantidad_cuotas_vencidas_mes[month][1] = (
                    cantidad_cuotas_vencidas_mes[month][1] + 1
                )

    # Calcular variación MoM por mes usando el conteo (posición 1)
    month_order = [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    ]
    prev_count = None
    for m in month_order:
        current_count = cantidad_cuotas_vencidas_mes[m][1]
        if prev_count in (None, 0):
            mom_str = "0%"
        else:
            change_pct = ((current_count - prev_count) / prev_count) * 100
            mom_str = f"{round(change_pct)}%"
        # tercer lugar: string porcentaje MoM
        cantidad_cuotas_vencidas_mes[m].append(mom_str)
        prev_count = current_count

    # Comparación entre meses seleccionados (el primero es la referencia)
    comparison = None
    if month_ref and month_cmp:
        ref_name = month_ref.value
        cmp_name = month_cmp.value
        if (
            ref_name in cantidad_cuotas_vencidas_mes
            and cmp_name in cantidad_cuotas_vencidas_mes
        ):
            # ref = previo, cmp = actual
            ref_count = cantidad_cuotas_vencidas_mes[ref_name][1]
            cmp_count = cantidad_cuotas_vencidas_mes[cmp_name][1]
            delta = cmp_count - ref_count
            direction = (
                "aumentó" if delta > 0 else ("disminuyó" if delta < 0 else "igual")
            )
            percent_str = (
                "no se puede comparar"
                if ref_count == 0
                else f"{round(((cmp_count - ref_count) / ref_count) * 100)}%"
            )
            comparison = {
                "reference_month": ref_name,
                "compare_month": cmp_name,
                "ref_count": ref_count,
                "cmp_count": cmp_count,
                "delta_abs": abs(delta),
                "direction": direction,
                "delta_percent": percent_str,
            }

    return {"installments": cantidad_cuotas_vencidas_mes, "comparison": comparison}
