from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from .base import BaseSchema, BaseResponseSchema, ListBase
from ..models.Client import ClientStateEnum

class ClientCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    document: str = Field(..., min_length=5, max_length=20, pattern=r'^[0-9]*')
    email: Optional[EmailStr] = None
    phone: str = Field(..., max_length=20)
    address: str = Field(..., max_length=255)
    zone: Optional[str] = Field(None, max_length=100)
    client_state: ClientStateEnum = ClientStateEnum.INACTIVE

    class Config:
        from_attributes = True

class ClientUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=255)
    zone: Optional[str] = Field(None, max_length=100)
    client_state: Optional[ClientStateEnum] = None
    
    class Config:
        from_attributes = True

class ClientResponse(BaseResponseSchema):
    name: str
    document: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    zone: Optional[str] = None
    client_state: ClientStateEnum

class ClientList(ListBase):
    items: List[ClientResponse]