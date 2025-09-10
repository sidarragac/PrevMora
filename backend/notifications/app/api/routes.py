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
    """
    Retrieve client alert data with phone, name, installments_value, and payment_date
    for clients that are in the Alert table.
    
    Returns ONE record per client-credit combination that has alerts,
    using the most recent installment for each combination.
    
    Returns data in the format:
    [
        {"to": "+573007465380", "name": "Alejo", "amount": "200.000", "date": "2025-09-20"},
        {"to": "+573012706204", "name": "Wambi", "amount": "200.000", "date": "2025-09-05"},
        ...
    ]
    """
    
    # Query to get one record per client-credit pair that has alerts
    # We'll get the most recent installment for each client-credit combination
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
    
    # Main query joining with the latest installment per client-credit pair
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
    
    # Format response according to requested structure
    response = []
    for row in rows:
        phone, name, amount, payment_date = row
        
        # Format amount as string with thousands separator
        formatted_amount = f"{float(amount):,.0f}".replace(",", ".")
        
        # Format payment_date
        formatted_date = payment_date.strftime("%Y-%m-%d") if payment_date else None
        
        response.append({
            "to": phone,
            "name": name,
            "amount": formatted_amount,
            "date": formatted_date
        })
    
    return response
