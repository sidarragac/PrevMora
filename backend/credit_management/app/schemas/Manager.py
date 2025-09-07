from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

from backend.credit_management.scripts.models import ManagerZone
from .base import BaseSchema, BaseResponseSchema
from ..models.Manager import ManagerZoneEnum

class ManagerCreate(BaseSchema):
    name: str = Field(..., min_length=1, max_length=100)
    manager_zone: ManagerZoneEnum
    
    class Config:
        orm_mode = True

class ManagerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    manager_zone: Optional[ManagerZoneEnum] = None

    class Config:
        orm_mode = True

class ManagerResponse(BaseResponseSchema):
    name: str
    manager_zone: ManagerZoneEnum

class ManagerList(BaseModel):
    items: List[ManagerResponse]
    total: int
    page: int
    page_size: int
    pages: int