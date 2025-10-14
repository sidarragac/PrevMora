from fastapi import APIRouter, Depends
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

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

    # Get current date and date 10 days from now
    current_date = datetime.now().date()
    ten_days_future = current_date + timedelta(days=10)

    query = (
        select(
            Client.phone,
            Client.name,
            Installment.installments_value,
            Installment.due_date
        )
        .select_from(subquery)
        .join(Client, subquery.c.client_id == Client.id)
        .join(Installment, subquery.c.latest_installment_id == Installment.id)
        .where(
            and_(
                Installment.due_date >= current_date,
                Installment.due_date <= ten_days_future
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
        
        recipients.append({
            "to": phone,
            "name": name,
            "amount": formatted_amount,
            "date": formatted_date
        })
    
    response = {
        "phone_number": "default",
        "language": "Spanish (MEX)",
        "recipients": recipients
    }
    
    return response
