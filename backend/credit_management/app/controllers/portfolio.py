from .base import BaseController
from ..models.Portfolio import Portfolio
from ..schemas.Portfolio import PortfolioResponse, PortfolioCreate, PortfolioUpdate, PortfolioList


class PortfolioController(BaseController):
    """Controller for Portfolio operations."""
    
    def __init__(self):
        super().__init__(
            model=Portfolio,
            get_schema=PortfolioResponse,
            create_schema=PortfolioCreate,
            update_schema=PortfolioUpdate,
            list_schema=PortfolioList,
            not_found_message="Portfolio not found"
        )

