from typing import Any, Generic, Optional, Type, TypeVar

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.base import Base
from ..repository.base import BaseRepository
from ..schemas.base import BaseResponseSchema, BaseSchema, PaginationParams

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseSchema)
GetSchemaType = TypeVar("GetSchemaType", bound=BaseResponseSchema)
ListSchemaType = TypeVar("ListSchemaType")


class BaseController(
    Generic[
        ModelType, CreateSchemaType, UpdateSchemaType, GetSchemaType, ListSchemaType
    ]
):
    """
    Base controller for common CRUD operations.
    """

    def __init__(
        self,
        model: Type[ModelType],
        get_schema: Type[GetSchemaType],
        create_schema: Type[CreateSchemaType],
        update_schema: Optional[Type[UpdateSchemaType]] = None,
        list_schema: Optional[Type[ListSchemaType]] = None,
        not_found_message: str = "Resource not found",
    ):
        self.model = model
        self.get_schema = get_schema
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.list_schema = list_schema
        self.not_found_message = not_found_message

    def _get_repository(self) -> BaseRepository:
        """Create and return a repository instance."""
        return BaseRepository(
            model=self.model, get_schema=self.get_schema, list_schema=self.list_schema
        )

    async def get_by_id(self, session: AsyncSession, resource_id: int) -> GetSchemaType:
        """Get a resource by ID."""
        repository = self._get_repository()
        resource = await repository.get_by_id(session, resource_id)
        if not resource:
            raise HTTPException(status_code=404, detail=self.not_found_message)
        return resource

    async def get_multi_paginated(
        self, session: AsyncSession, pagination: PaginationParams
    ) -> ListSchemaType:
        """Get multiple resources with pagination."""
        repository = self._get_repository()
        return await repository.get_multi_paginated(session, pagination)

    async def create(
        self, session: AsyncSession, resource_data: CreateSchemaType
    ) -> GetSchemaType:
        """Create a new resource."""
        repository = self._get_repository()
        return await repository.create(session, resource_data)

    async def update(
        self, session: AsyncSession, resource_id: int, update_data: UpdateSchemaType
    ) -> GetSchemaType:
        """Update an existing resource."""
        if not self.update_schema:
            raise HTTPException(
                status_code=405, detail="Update operation not supported"
            )

        repository = self._get_repository()
        updated_resource = await repository.update(session, resource_id, update_data)
        if not updated_resource:
            raise HTTPException(status_code=404, detail=self.not_found_message)
        return updated_resource
