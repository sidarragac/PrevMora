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

class PaginationParams:
    def __init__(self, page: int = 1, page_size: int = 10):
        self.page = page
        self.page_size = page_size
        self.skip = (page - 1) * page_size

class PaginatedResponse(Generic[T]):
    def __init__(
        self, 
        items: list[T], 
        total: int, 
        page: int = 1, 
        page_size: int = 10
    ):
        self.items = items
        self.total = total
        self.page = page
        self.page_size = page_size
        self.pages = (total + page_size - 1) // page_size if total > 0 else 0