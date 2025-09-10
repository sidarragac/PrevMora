from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from .base import BaseResponseSchema, BaseSchema, ListBase


class ManagerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    manager_zone: str

    class Config:
        from_attributes = True


class ManagerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    manager_zone: Optional[str] = None

    class Config:
        from_attributes = True


class ManagerResponse(BaseResponseSchema):
    name: str
    manager_zone: str


class ManagerList(ListBase):
    items: List[ManagerResponse]
