from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.Portfolio import Portfolio
from ..repository.portfolio import PortfolioRepository
from ..schemas.Portfolio import (
    PortfolioCreate,
    PortfolioList,
    PortfolioResponse,
    PortfolioUpdate,
)
from ..schemas.base import PaginationParams
from .base import BaseController


class PortfolioController(BaseController):
    """Controller for Portfolio operations."""

    def __init__(self):
        super().__init__(
            model=Portfolio,
            get_schema=PortfolioResponse,
            create_schema=PortfolioCreate,
            update_schema=PortfolioUpdate,
            list_schema=PortfolioList,
            not_found_message="Portfolio not found",
        )

    def _get_repository(self) -> PortfolioRepository:
        """Create and return a custom portfolio repository instance."""
        return PortfolioRepository()

    async def get_by_id(self, session: AsyncSession, resource_id: int) -> PortfolioResponse:
        """Get a portfolio by ID with manager information."""
        repository = self._get_repository()
        resource = await repository.get_by_id(session, resource_id)
        if not resource:
            raise HTTPException(status_code=404, detail=self.not_found_message)
        return resource

    async def get_multi_paginated(
        self, session: AsyncSession, pagination: PaginationParams
    ) -> PortfolioList:
        """Get multiple portfolios with pagination and manager information."""
        repository = self._get_repository()
        return await repository.get_multi_paginated(session, pagination)
