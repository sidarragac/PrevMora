from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from .base import BaseSchema, BaseResponseSchema
from ..models.Portfolio import ContactResultEnum, ContactMethodEnum

class PortfolioCreate(BaseSchema):
    installment_id: int = Field(..., gt=0)
    manager_id: int = Field(..., gt=0)
    contact_method: ContactMethodEnum
    contact_result: ContactResultEnum
    management_date: date
    observation: Optional[str] = None
    payment_promise_date: Optional[date] = None
    
    class Config:
        orm_mode = True

class PortfolioUpdate(BaseSchema):
    contact_method: Optional[ContactMethodEnum] = None
    contact_result: Optional[ContactResultEnum] = None
    management_date: Optional[date] = None
    observation: Optional[str] = None
    payment_promise_date: Optional[date] = None
    
    class Config:
        orm_mode = True

class PortfolioResponse(BaseResponseSchema):
    installment_id: int
    manager_id: int
    contact_method: ContactMethodEnum
    contact_result: ContactResultEnum
    management_date: date
    observation: Optional[str] = None
    payment_promise_date: Optional[date] = None

class PortfolioList(BaseModel):
    items: List[PortfolioResponse]
    total: int
    page: int
    page_size: int
    pages: int