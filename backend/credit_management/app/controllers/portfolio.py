from ..models.Portfolio import Portfolio
from ..schemas.Portfolio import (
    PortfolioCreate,
    PortfolioList,
    PortfolioResponse,
    PortfolioUpdate,
)
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
