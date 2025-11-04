from typing import Dict, List

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.installment import Installment
from app.models.portafolio import Portfolio
from app.models.manager import Manager
from app.models.credit import Credit
from app.models.client import Client


# Lista de meses en español en orden
MONTHS: List[str] = [
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


async def fetch_portfolio(session: AsyncSession) -> Dict:
    """Obtiene items de `Portfolio` y retorna items y cantidad."""
    query = select(
        Portfolio.id,
        Portfolio.installment_id,
        Portfolio.management_date,
        Portfolio.contact_method,
        Portfolio.contact_result,
        Portfolio.observation,
        Portfolio.payment_promise_date,
        Portfolio.manager_id,
        Portfolio.created_at,
        Portfolio.updated_at,
    )
    result = await session.execute(query)
    rows = result.mappings().all()
    items = [dict(r) for r in rows]
    return {"items": items, "count": len(items)}


def _empty_month_buckets() -> Dict[str, List[Dict]]:
    return {month: [] for month in MONTHS}


def _month_name_from_date(date_obj) -> str | None:
    if not date_obj:
        return None
    month_index = date_obj.month  # 1..12
    return MONTHS[month_index - 1]


async def calculate_installments_by_month(session: AsyncSession) -> Dict:
    """Agrupa cuotas por mes, calcula morosidad y saldos por mes."""
    base_query = select(
        Installment.id,
        Installment.credit_id,
        Installment.installments_number,
        Installment.due_date,
        Installment.installments_value,
        Installment.installment_state,
        Installment.payment_date,
    )
    base_result = await session.execute(base_query)
    base_rows = base_result.fetchall()

    installments_grouped: Dict[str, List[Dict]] = _empty_month_buckets()
    for (
        id_,
        credit_id,
        installments_number,
        due_date,
        installments_value,
        installment_state,
        payment_date,
    ) in base_rows:
        month_name = _month_name_from_date(due_date)
        if not month_name:
            continue
        item = {
            "id": id_,
            "credit_id": credit_id,
            "installments_number": installments_number,
            "due_date": due_date.strftime("%Y-%m-%d") if due_date else None,
            "installments_value": float(installments_value),
            "installment_state": installment_state,
            "payment_date": payment_date.strftime("%Y-%m-%d") if payment_date else None,
        }
        installments_grouped[month_name].append(item)

    overdue_query = base_query.where(
        or_(
            and_(
                Installment.payment_date.is_not(None),
                Installment.payment_date > Installment.due_date,
            ),
            Installment.installment_state == "Vencida",
        )
    )
    overdue_result = await session.execute(overdue_query)
    overdue_rows = overdue_result.fetchall()

    overdue_grouped: Dict[str, List[Dict]] = _empty_month_buckets()
    for (
        id_,
        credit_id,
        installments_number,
        due_date,
        installments_value,
        installment_state,
        payment_date,
    ) in overdue_rows:
        month_name = _month_name_from_date(due_date)
        if not month_name:
            continue
        item = {
            "id": id_,
            "credit_id": credit_id,
            "installments_number": installments_number,
            "due_date": due_date.strftime("%Y-%m-%d") if due_date else None,
            "installments_value": float(installments_value),
            "installment_state": installment_state,
            "payment_date": payment_date.strftime("%Y-%m-%d") if payment_date else None,
        }
        overdue_grouped[month_name].append(item)

    porcentaje_morosidad: List[str] = []
    comparacion_mes_anterior: List[str] = []
    for month in MONTHS:
        total = len(installments_grouped[month])
        overdue = len(overdue_grouped[month])
        if total == 0 or overdue == 0:
            porcentaje_morosidad.append("0")
        else:
            porcentaje_morosidad.append(f"{(overdue / total) * 100}")

    for i, value in enumerate(porcentaje_morosidad):
        if i == 0:
            comparacion_mes_anterior.append("0")
        else:
            comparacion_mes_anterior.append(
                f"{(float(porcentaje_morosidad[i]) - float(porcentaje_morosidad[i-1]))}"
            )

    datos = [
        f"Total de cuotas en {MONTHS[i]}: {len(installments_grouped[MONTHS[i]])}, "
        f"Numero de cuotas Vencidas: {len(overdue_grouped[MONTHS[i]])}, "
        f"Porcentaje  Morosidad: {porcentaje_morosidad[i]}%"
        + (", comparacion con el mes anterior: " + comparacion_mes_anterior[i] if i > 0 else ", comparacion con el mes anterior: 0")
        for i in range(12)
    ]

    deuda_por_mes = [0.0] * 12
    monto_por_mes = [0.0] * 12
    balance_por_mes = [0.0] * 12

    for i, month in enumerate(MONTHS):
        for item in installments_grouped[month]:
            payment_date = item["payment_date"]
            due_date = item["due_date"]
            value = float(item["installments_value"])
            if payment_date is not None:
                if payment_date > due_date:
                    deuda_por_mes[i] += value
                else:
                    monto_por_mes[i] += value
            if item["installment_state"] == "Vencida":
                deuda_por_mes[i] += value

    for i in range(12):
        balance_por_mes[i] = monto_por_mes[i] - deuda_por_mes[i]

    return {
        "installments": installments_grouped,
        "datos": datos,
        "DeudaPorMes": deuda_por_mes,
        "MontoPorMes": monto_por_mes,
        "BalancePorMes": balance_por_mes,
    }


async def calculate_money_recovery_by_month(session: AsyncSession) -> Dict:
    """Calcula recuperación de dinero por mes y métricas asociadas."""
    query = select(
        Installment.id,
        Installment.credit_id,
        Installment.installments_number,
        Installment.due_date,
        Installment.installments_value,
        Installment.installment_state,
        Installment.payment_date,
    )
    result = await session.execute(query)
    rows = result.fetchall()

    grouped = _empty_month_buckets()

    for (
        id_,
        credit_id,
        installments_number,
        due_date,
        installments_value,
        installment_state,
        payment_date,
    ) in rows:
        month_name = _month_name_from_date(due_date)
        if not month_name:
            continue
        item = {
            "id": id_,
            "credit_id": credit_id,
            "installments_number": installments_number,
            "due_date": due_date.strftime("%Y-%m-%d") if due_date else None,
            "installments_value": float(installments_value),
            "installment_state": installment_state,
            "payment_date": payment_date.strftime("%Y-%m-%d") if payment_date else None,
        }
        grouped[month_name].append(item)

    recuperacion_por_mes = [0.0] * 12
    porcentaje_recuperacion_por_mes = [0.0] * 12
    deuda_total_por_mes = [0.0] * 12

    for i, month in enumerate(MONTHS):
        for item in grouped[month]:
            value = float(item["installments_value"])
            if item["payment_date"] is not None:
                if item["payment_date"] > item["due_date"]:
                    recuperacion_por_mes[i] += value
                    deuda_total_por_mes[i] += value
            if item["installment_state"] == "Vencida":
                deuda_total_por_mes[i] += value

    for i in range(12):
        if recuperacion_por_mes[i] == 0:
            porcentaje_recuperacion_por_mes[i] = 0
        else:
            porcentaje_recuperacion_por_mes[i] = (
                recuperacion_por_mes[i] / deuda_total_por_mes[i] * 100
                if deuda_total_por_mes[i] != 0
                else 0
            )

    return {
        "RecuperacionPorMes": recuperacion_por_mes,
        "DeudaTotalPorMes": deuda_total_por_mes,
        "PorcentajeRecuperacionPorMes": porcentaje_recuperacion_por_mes,
    }


async def average_recovery_for_selected_months(
    selected_months: List[str], session: AsyncSession
) -> Dict:
    """Calcula el promedio de recuperación para un subconjunto de meses."""
    datos = await calculate_money_recovery_by_month(session)
    recuperacion = datos["RecuperacionPorMes"]
    indices = [MONTHS.index(mes) for mes in selected_months]
    valores = [recuperacion[i] for i in indices]
    promedio = sum(valores) / len(valores) if valores else 0
    return {
        "seleccion": selected_months,
        "valores": valores,
        "promedio_recuperacion": promedio,
    }


# Contactos por manager + lista de clientes contactados
async def contacts_by_manager(session: AsyncSession) -> Dict:
    query = (
        select(
            Portfolio.id.label("portfolio_id"),
            Manager.id.label("manager_id"),
            Manager.name.label("manager_name"),
            Client.id.label("client_id"),
            Client.name.label("client_name"),
        )
        .join(Installment, Portfolio.installment_id == Installment.id)
        .join(Credit, Installment.credit_id == Credit.id)
        .join(Client, Credit.client_id == Client.id)
        .join(Manager, Portfolio.manager_id == Manager.id)
    )

    result = await session.execute(query)
    rows = result.mappings().all()

    by_manager: Dict[int, Dict] = {}
    for r in rows:
        m_id = r["manager_id"]
        m_name = r["manager_name"]
        c_id = r["client_id"]
        c_name = r["client_name"]
        if m_id not in by_manager:
            by_manager[m_id] = {
                "manager_id": m_id,
                "manager_name": m_name,
                "contacts_count": 0,
                "clients": {},  # temp dict to dedupe by client_id
            }
        by_manager[m_id]["contacts_count"] += 1
        by_manager[m_id]["clients"][c_id] = {"id": c_id, "name": c_name}

    items = []
    for m in by_manager.values():
        clients_list = list(m["clients"].values())
        items.append(
            {
                "manager_id": m["manager_id"],
                "manager_name": m["manager_name"],
                "contacts_count": m["contacts_count"],
                "clients": clients_list,
                "unique_clients_count": len(clients_list),
            }
        )

    # Orden opcional por mayor número de contactos
    items.sort(key=lambda x: x["contacts_count"], reverse=True)
    return {"items": items, "count": len(items)}

