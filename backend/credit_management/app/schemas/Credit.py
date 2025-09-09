from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
from .base import BaseSchema, BaseResponseSchema
from ..models.Credit import CreditStateEnum

class CreditCreate(BaseSchema):
    client_id: int
    disbursement_amount: int = Field(..., gt=0)
    payment_reference: int = Field(..., gt=0)
    interest_rate: float
    total_quotas: int = Field(..., gt=0)
    disbursement_date: date
    credit_state: CreditStateEnum = CreditStateEnum.PENDING
    
    class Config:
        orm_mode = True

class CreditUpdate(BaseSchema):
    disbursement_amount: Optional[int] = Field(None, gt=0)
    interest_rate: Optional[float | int] = Field(None, ge=0)
    total_quotas: Optional[int] = Field(None, gt=0)
    credit_state: Optional[CreditStateEnum] = None

    class Config:
        orm_mode = True

class CreditResponse(BaseResponseSchema):
    id: int
    client_id: int
    disbursement_amount: int
    payment_reference: int
    interest_rate: float | int
    total_quotas: int
    disbursement_date: date
    credit_state: CreditStateEnum

class CreditList(BaseModel):
    items: List[CreditResponse]
    total: int
    page: int
    page_size: int
    pages: int