from datetime import datetime
from typing import Optional, Any, TypeVar, Generic
from pydantic import BaseModel, Field

T = TypeVar('T')

class BaseSchema(BaseModel):
    id: Optional[int] = None
    
    class Config:
        orm_mode = True

class BaseResponseSchema(BaseSchema):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 10
    
    @property
    def skip(self) -> int:
        return (self.page - 1) * self.page_size

class ListBase(BaseModel):
    total: int
    page: int
    page_size: int
    pages: int