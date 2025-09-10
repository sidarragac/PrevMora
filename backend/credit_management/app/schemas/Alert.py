from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from .base import BaseResponseSchema, BaseSchema, ListBase


class AlertCreate(BaseModel):
    credit_id: int = Field(..., gt=0)
    client_id: int = Field(..., gt=0)
    alert_type: str
    manually_generated: bool
    alert_date: date

    class Config:
        from_attributes = True


# This does not make sense in the current model, domain logic, and requirements
# class AlertUpdate(BaseSchema):
#     credit_id: Optional[int] = None
#     alert_type: Optional[AlertTypeEnum] = None
#     manually_generated: Optional[bool] = None
#     alert_date: Optional[datetime] = None
#     class Config:
#         orm_mode = True


class AlertResponse(BaseResponseSchema):
    credit_id: int = Field(..., gt=0)
    client_id: int = Field(..., gt=0)
    alert_type: str
    manually_generated: bool
    alert_date: date


class AlertList(ListBase):
    items: List[AlertResponse]
