from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

from .base import BaseSchema, BaseResponseSchema, ListBase
from ..models.Manager import ManagerZoneEnum

class ManagerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    manager_zone: ManagerZoneEnum
    
    class Config:
        from_attributes = True

class ManagerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    manager_zone: Optional[ManagerZoneEnum] = None

    class Config:
        from_attributes = True

class ManagerResponse(BaseResponseSchema):
    name: str
    manager_zone: ManagerZoneEnum

class ManagerList(ListBase):
    items: List[ManagerResponse]