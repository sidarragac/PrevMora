from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List
from datetime import datetime, date
from .base import BaseSchema, BaseResponseSchema, ListBase
from ..models.Credit import INTEREST_RATE_MULTIPLIER

class CreditCreate(BaseModel):
    client_id: int
    disbursement_amount: int = Field(..., gt=0)
    payment_reference: str = Field(..., min_length=1)
    interest_rate: float
    total_quotas: int = Field(..., gt=0)
    disbursement_date: date
    credit_state: str = "Pendiente"
    
    class Config:
        from_attributes = True

    @classmethod
    def convert_rates_to_db(cls, data):
        if isinstance(data, dict) and 'interest_rate' in data:
            data['interest_rate'] = int(data['interest_rate'] * INTEREST_RATE_MULTIPLIER)
        return data

class CreditUpdate(BaseModel):
    disbursement_amount: Optional[int] = Field(None, gt=0)
    interest_rate: Optional[float] = Field(None, ge=0)
    total_quotas: Optional[int] = Field(None, gt=0)
    credit_state: Optional[str] = None

    class Config:
        from_attributes = True

class CreditResponse(BaseResponseSchema):
    id: int
    client_id: int
    disbursement_amount: int
    payment_reference: str
    interest_rate: float
    total_quotas: int
    disbursement_date: date
    credit_state: str

    @field_validator('interest_rate', mode='before')
    @classmethod
    def convert_interest_rate(cls, v):
        if isinstance(v, int):
            return v / INTEREST_RATE_MULTIPLIER
        return v

class CreditList(ListBase):
    items: List[CreditResponse]