from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..config.database import get_db_session
from ..models.alert import Alert
from ..models.client import Client
from ..models.credit import Credit
from ..models.installment import Installment

router = APIRouter()


@router.get("/client-alerts")
async def get_client_alerts(db: AsyncSession = Depends(get_db_session)):
    subquery = (
        select(
            Alert.client_id,
            Alert.credit_id,
            func.max(Installment.id).label("latest_installment_id")
        )
        .select_from(Alert)
        .join(Installment, Alert.credit_id == Installment.credit_id)
        .group_by(Alert.client_id, Alert.credit_id)
    ).subquery()

    query = (
        select(
            Client.phone,
            Client.name,
            Installment.installments_value,
            Installment.payment_date
        )
        .select_from(subquery)
        .join(Client, subquery.c.client_id == Client.id)
        .join(Installment, subquery.c.latest_installment_id == Installment.id)
    )
    
    result = await db.execute(query)
    rows = result.fetchall()

    response = []
    for row in rows:
        phone, name, amount, payment_date = row

        formatted_amount = f"{float(amount):,.0f}".replace(",", ".")

        formatted_date = payment_date.strftime("%Y-%m-%d") if payment_date else None
        
        response.append({
            "to": phone,
            "name": name,
            "amount": formatted_amount,
            "date": formatted_date
        })
    
    return response
