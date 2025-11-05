from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from .base import BaseResponseSchema, BaseSchema, ListBase


class PortfolioCreate(BaseModel):
    installment_id: int = Field(..., gt=0)
    manager_id: int = Field(..., gt=0)
    contact_method: str
    contact_result: str
    management_date: date
    observation: Optional[str] = None
    payment_promise_date: Optional[date] = None

    class Config:
        from_attributes = True


class PortfolioUpdate(BaseModel):
    contact_method: Optional[str] = None
    contact_result: Optional[str] = None
    management_date: Optional[date] = None
    observation: Optional[str] = None
    payment_promise_date: Optional[date] = None

    class Config:
        from_attributes = True


class PortfolioResponse(BaseResponseSchema):
    installment_id: int
    manager_id: int
    manager_name: str
    contact_method: str
    contact_result: str
    management_date: date
    observation: Optional[str] = None
    payment_promise_date: Optional[date] = None


class PortfolioList(ListBase):
    items: List[PortfolioResponse]
