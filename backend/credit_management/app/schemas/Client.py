from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from .base import BaseSchema, BaseResponseSchema, ListBase
from ..models.Credit import INTEREST_RATE_MULTIPLIER

class ClientCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    document: str = Field(..., min_length=5, max_length=20, pattern=r'^[0-9]*')
    email: Optional[EmailStr] = None
    phone: str = Field(..., max_length=20)
    address: str = Field(..., max_length=255)
    zone: Optional[str] = Field(None, max_length=100)
    status: str = "Inactivo"

    class Config:
        from_attributes = True

class ClientUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=255)
    zone: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = None
    
    class Config:
        from_attributes = True

class ClientResponse(BaseResponseSchema):
    name: str
    document: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    zone: Optional[str] = None
    status: str

class ClientList(ListBase):
    items: List[ClientResponse]

# Schemas para el endpoint completo del cliente
class PortfolioDetailResponse(BaseModel):
    id: int
    installment_id: int
    manager_id: int
    contact_method: str
    contact_result: str
    management_date: date
    observation: Optional[str] = None
    payment_promise_date: Optional[date] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class InstallmentDetailResponse(BaseModel):
    id: int
    credit_id: int
    installment_state: str
    installments_number: int
    installments_value: Decimal
    due_date: date
    payment_date: Optional[date] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # Gestiones de cartera asociadas a esta cuota
    portfolio: List[PortfolioDetailResponse] = []

    class Config:
        from_attributes = True

class CreditDetailResponse(BaseModel):
    id: int
    client_id: int
    disbursement_amount: int
    payment_reference: str
    interest_rate: float
    total_quotas: int
    disbursement_date: date
    credit_state: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # Cuotas asociadas a este crédito
    installments: List[InstallmentDetailResponse] = []

    @field_validator('interest_rate', mode='before')
    @classmethod
    def convert_interest_rate(cls, v):
        if isinstance(v, int):
            return v / INTEREST_RATE_MULTIPLIER
        return v

    class Config:
        from_attributes = True

class AlertDetailResponse(BaseModel):
    id: int
    credit_id: int
    client_id: int
    alert_type: str
    manually_generated: bool
    alert_date: date
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ReconciliationDetailResponse(BaseModel):
    id: int
    transaction_date: date
    payment_reference: str
    payment_amount: int
    payment_channel: str
    observation: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ClientCompleteResponse(BaseModel):
    # Datos básicos del cliente
    id: int
    name: str
    document: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    zone: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Datos relacionados
    credits: List[CreditDetailResponse] = []
    alerts: List[AlertDetailResponse] = []
    reconciliations: List[ReconciliationDetailResponse] = []
    
    # Estadísticas resumen
    total_credits: int = 0
    total_installments: int = 0
    total_portfolio_managements: int = 0
    total_alerts: int = 0
    total_reconciliations: int = 0

    class Config:
        from_attributes = True