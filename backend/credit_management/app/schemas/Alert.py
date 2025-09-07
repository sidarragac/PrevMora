from pydantic import Field, BaseModel
from typing import Optional, List
from datetime import datetime
from .base import BaseResponseSchema, BaseSchema
from ..models.Alert import AlertTypeEnum

class AlertCreate(BaseSchema):
    credit_id: int = Field(..., gt=0)
    alert_type: AlertTypeEnum
    manually_generated: bool
    alert_date: datetime

    class Config:
        orm_mode = True

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

class AlertList(BaseModel):
    items: List[AlertResponse]
    total: int
    page: int
    page_size: int
    pages: int