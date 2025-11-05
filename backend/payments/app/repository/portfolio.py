from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..models.Manager import Manager
from ..models.Portfolio import Portfolio
from ..schemas.base import PaginationParams
from ..schemas.Portfolio import PortfolioList, PortfolioResponse
from .base import BaseRepository


class PortfolioRepository(BaseRepository):
    """Custom repository for Portfolio with Manager joins."""

    def __init__(self):
        super().__init__(
            model=Portfolio,
            get_schema=PortfolioResponse,
            list_schema=PortfolioList,
        )

    async def get_by_id(self, db: AsyncSession, id: int) -> PortfolioResponse | None:
        """Get portfolio by ID with manager information."""
        result = await db.execute(
            select(Portfolio)
            .where(Portfolio.id == id)
            .options(joinedload(Portfolio.manager))
        )
        db_obj = result.scalar_one_or_none()
        if db_obj:
            return self._to_response_schema(db_obj)
        return None

    async def get_multi_paginated(
        self,
        db: AsyncSession,
        pagination: PaginationParams,
        estimate_count: bool = True,
    ) -> PortfolioList:
        """Get paginated portfolios with manager information."""
        from sqlalchemy import func

        # Get items with manager data
        result = await db.execute(
            select(Portfolio)
            .options(joinedload(Portfolio.manager))
            .offset(pagination.skip)
            .limit(pagination.page_size + 1)
            .order_by(Portfolio.id)
        )
        db_items = result.unique().scalars().all()

        has_next = len(db_items) > pagination.page_size
        if has_next:
            db_items = db_items[:-1]

        total = 0
        pages = 0

        if estimate_count:
            total_result = await db.execute(select(func.count()).select_from(Portfolio))
            total = total_result.scalar_one()
            pages = (
                (total + pagination.page_size - 1) // pagination.page_size
                if total > 0
                else 0
            )

        items = [self._to_response_schema(item) for item in db_items]

        return PortfolioList(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            pages=pages,
            has_next=has_next,
        )

    def _to_response_schema(self, db_obj: Portfolio) -> PortfolioResponse:
        """Convert Portfolio model to response schema with manager name."""
        return PortfolioResponse(
            id=db_obj.id,
            installment_id=db_obj.installment_id,
            manager_id=db_obj.manager_id,
            manager_name=db_obj.manager.name,
            contact_method=db_obj.contact_method,
            contact_result=db_obj.contact_result,
            management_date=db_obj.management_date,
            observation=db_obj.observation,
            payment_promise_date=db_obj.payment_promise_date,
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at,
        )
