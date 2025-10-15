from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field

from .base import BaseResponseSchema, BaseSchema, ListBase


class InstallmentCreate(BaseModel):
    credit_id: int = Field(..., gt=0)
    installment_state: str
    installments_number: int = Field(..., gt=0)
    installments_value: Decimal = Field(..., gt=0)
    due_date: date
    payment_date: Optional[date] = Field(None)

    class Config:
        from_attributes = True


# This schema can be used for updating installments if needed in the future
# Currently it does not make sense on the business logic
# Changed
class InstallmentUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0)
    due_date: Optional[date] = None
    state: Optional[str] = None
    payment_date: Optional[date] = None
    installment_state: Optional[str] = None
    payment_amount: Optional[Decimal] = Field(None, gt=0)
    payment_channel: Optional[str] = None

    class Config:
        orm_mode = True


class InstallmentResponse(BaseResponseSchema):
    credit_id: int
    installment_state: str
    installments_number: int
    installments_value: Decimal
    due_date: date
    payment_date: Optional[date] = None


class InstallmentList(ListBase):
    items: List[InstallmentResponse]
