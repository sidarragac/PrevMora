from ..models.Credit import Credit
from ..schemas.Credit import CreditCreate, CreditList, CreditResponse, CreditUpdate
from .base import BaseController


class CreditController(BaseController):
    """Controller for Credit operations."""

    def __init__(self):
        super().__init__(
            model=Credit,
            get_schema=CreditResponse,
            create_schema=CreditCreate,
            update_schema=CreditUpdate,
            list_schema=CreditList,
            not_found_message="Credit not found",
        )
