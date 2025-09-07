from datetime import date
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
from decimal import Decimal
from .base import BaseSchema, BaseResponseSchema
from ..models.Installment import InstallmentStateEnum

class InstallmentCreate(BaseSchema):
    credit_id: int = Field(..., gt=0)
    installment_state: InstallmentStateEnum
    installment_number: int = Field(..., gt=0)
    installment_value: int = Field(..., gt=0)
    due_date: date
    payment_date: Optional[date] = Field(None)
    
    class Config:
        orm_mode = True

# This schema can be used for updating installments if needed in the future
# Currently it does not make sense on the business logic
# class InstallmentUpdate(BaseModel):
#     amount: Optional[Decimal] = Field(None, gt=0)
#     due_date: Optional[date] = None
#     state: Optional[InstallmentStateEnum] = None
#     payment_date: Optional[date] = None
#     payment_amount: Optional[Decimal] = Field(None, gt=0)
#     payment_channel: Optional[PaymentChannel] = None
    
#     class Config:
#         orm_mode = True

class InstallmentResponse(BaseResponseSchema):
    credit_id: int
    installment_state: InstallmentStateEnum
    installment_number: int
    installment_value: int
    due_date: date
    payment_date: Optional[date] = None

class InstallmentList(BaseModel):
    items: List[InstallmentResponse]
    total: int
    page: int
    page_size: int
    pages: int