from functools import reduce
from typing import Any, Generic, Type, TypeVar, Optional
from pydantic import BaseModel

from sqlalchemy import Select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

from ..models.base import Base
from ..schemas.base import BaseSchema, BaseResponseSchema

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseSchema)
GetSchemaType = TypeVar("GetSchemaType", bound=BaseResponseSchema)

class BaseRepository(Generic[ModelType, CreateSchemaType, GetSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], 
                 create_schema: Type[CreateSchemaType] = None,
                 get_schema: Type[GetSchemaType] = None,
                 update_schema: Type[UpdateSchemaType] = None):
        self.model = model
        self.create_schema = create_schema
        self.get_schema = get_schema
        self.update_schema = update_schema

    async def get_by_id(self, db: AsyncSession, id: int) -> GetSchemaType | None:
        result = await db.execute(select(self.model).where(self.model.id == id))
        db_obj = result.scalar_one_or_none()
        if db_obj:
            return self.get_schema.model_validate(db_obj, from_attributes=True)
        return None

    # async def get_multi(
    #     self,
    #     db: AsyncSession,
    #     skip: int = 0,
    #     limit: int = 100,
    # ) -> list[ModelType]:
    #     result = await db.execute(
    #         select(self.model).offset(skip).limit(limit)
    #     )
    #     return result.scalars().all()

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