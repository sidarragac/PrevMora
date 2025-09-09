from functools import reduce
from typing import Any, Generic, Type, TypeVar, Optional
from pydantic import BaseModel

from sqlalchemy import Select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

from ..models.base import Base
from ..schemas.base import BaseSchema, BaseResponseSchema, PaginationParams

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseSchema)
GetSchemaType = TypeVar("GetSchemaType", bound=BaseResponseSchema)
ListSchemaType = TypeVar("ListSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, GetSchemaType, UpdateSchemaType, ListSchemaType]):
    def __init__(self, model: Type[ModelType], 
                 get_schema: Type[GetSchemaType] = None,
                 list_schema: Type[ListSchemaType] = None):
        self.model = model
        self.get_schema = get_schema
        self.list_schema = list_schema

    async def get_by_id(self, db: AsyncSession, id: int) -> GetSchemaType | None:
        result = await db.execute(select(self.model).where(self.model.id == id))
        db_obj = result.scalar_one_or_none()
        if db_obj:
            return self.get_schema.model_validate(db_obj, from_attributes=True)
        return None
    
    async def get_multi_paginated(
        self,
        db: AsyncSession,
        pagination: PaginationParams,
        estimate_count: bool = True
    ) -> ListSchemaType:

        result = await db.execute(
            select(self.model)
            .offset(pagination.skip)
            .limit(pagination.page_size + 1)
            .order_by(self.model.id)
        )
        db_items = result.scalars().all()
        
        has_next = len(db_items) > pagination.page_size
        if has_next:
            db_items = db_items[:-1]
        
        total = 0
        pages = 0
        
        if estimate_count:
            total_result = await db.execute(select(func.count()).select_from(self.model))
            total = total_result.scalar_one()
            pages = (total + pagination.page_size - 1) // pagination.page_size if total > 0 else 0
        
        items = [self.get_schema.model_validate(item, from_attributes=True) for item in db_items]
        
        return self.list_schema(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            pages=pages,
            has_next=has_next
        )

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> GetSchemaType:
        obj_data = obj_in.model_dump(exclude_unset=True)
        db_obj = self.model(**obj_data)
        db.add(db_obj)

        await db.commit()
        await db.refresh(db_obj)

        return self.get_schema.model_validate(db_obj, from_attributes=True)
    
    async def update(self, db: AsyncSession, id: int, obj_in: UpdateSchemaType) -> GetSchemaType | None:
        result = await db.execute(select(self.model).where(self.model.id == id))
        db_obj = result.scalar_one_or_none()
        
        if not db_obj:
            return None
        
        update_data = obj_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        
        return self.get_schema.model_validate(db_obj, from_attributes=True)


    # async def create(self, db: AsyncSession, obj_in: dict) -> ModelType:
    #     db_obj = self.model(**obj_in)  # type: ignore
    #     db.add(db_obj)
    #     await db.commit()
    #     await db.refresh(db_obj)
    #     return db_obj

    # async def update(
    #     self,
    #     db: AsyncSession,
    #     db_obj: ModelType,
    #     obj_in: dict,
    # ) -> ModelType:
    #     for field, value in obj_in.items():
    #         setattr(db_obj, field, value)
    #     db.add(db_obj)
    #     await db.commit()
    #     await db.refresh(db_obj)
    #     return db_obj

    # async def remove(self, db: AsyncSession, id: int) -> ModelType | None:
    #     obj = await self.get(db, id)
    #     if obj:
    #         await db.delete(obj)
    #         await db.commit()
    #         return obj
    #     return None

    # async def count(self, db: AsyncSession) -> int:
    #     result = await db.execute(select(func.count()).select_from(self.model))
    #     return result.scalar_one()