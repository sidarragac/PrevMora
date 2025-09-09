from pydantic import Field, BaseModel
from typing import Optional, List
from datetime import datetime
from .base import BaseResponseSchema, BaseSchema, ListBase
from ..models.Alert import AlertTypeEnum

class AlertCreate(BaseModel):
    credit_id: int = Field(..., gt=0)
    alert_type: AlertTypeEnum
    manually_generated: bool
    alert_date: datetime

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
    alert_type: AlertTypeEnum
    manually_generated: bool
    alert_date: datetime

class AlertList(ListBase):
    items: List[AlertResponse]