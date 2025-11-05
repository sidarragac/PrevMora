from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config.database import get_db_session
from ..models.client import Client
from ..models.credit import Credit
from ..models.installment import Installment

router = APIRouter()


@router.get("/client-alerts")
async def get_client_alerts(db: AsyncSession = Depends(get_db_session)):
    # Get current date and date 10 days from now
    current_date = datetime.now().date()
    ten_days_future = current_date + timedelta(days=10)

    # Select clients by upcoming installment due dates (no alerts involved)
    query = (
        select(
            Client.phone,
            Client.name,
            Installment.installments_value,
            Installment.due_date,
        )
        .select_from(Installment)
        .join(Credit, Installment.credit_id == Credit.id)
        .join(Client, Credit.client_id == Client.id)
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
                # "template": "moroso2"
            }
        )

    response = {
        "phone_number": "default",
        "language": "Spanish (MEX)",
        "recipients": recipients,
    }

    return response
