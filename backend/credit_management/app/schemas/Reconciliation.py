from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from .base import BaseSchema, BaseResponseSchema, ListBase
from ..models.Reconciliation import PaymentChanelEnum

class ReconciliationCreate(BaseModel):
    payment_channel: PaymentChanelEnum
    payment_reference: int = Field(..., gt=0)
    payment_amount: int = Field(..., gt=0)
    transaction_date: date
    observation: Optional[str] = None
    
    class Config:
        from_attributes = True

# This does not make sense in the current model, domain logic, and requirements
# class ReconciliationUpdate(BaseSchema):
#     payment_channel: Optional[PaymentChanelEnum] = None
#     payment_amount: Optional[int] = Field(None, gt=0)
#     transaction_date: Optional[date] = None
#     observation: Optional[str] = None
    
#     class Config:
#         orm_mode = True

class ReconciliationResponse(BaseResponseSchema):
    payment_channel: PaymentChanelEnum
    payment_reference: int
    payment_amount: int
    transaction_date: date
    observation: Optional[str] = None

class ReconciliationList(ListBase):
    items: List[ReconciliationResponse]