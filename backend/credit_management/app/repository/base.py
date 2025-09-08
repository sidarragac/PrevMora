from functools import reduce
from typing import Any, Generic, Type, TypeVar

from sqlalchemy import Select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

from ..models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_id(self, db: AsyncSession, id: int) -> ModelType | None:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

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