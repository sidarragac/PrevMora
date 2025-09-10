from .base import BaseController
from ..models.Credit import Credit
from ..schemas.Credit import CreditResponse, CreditCreate, CreditUpdate, CreditList


class CreditController(BaseController):
    """Controller for Credit operations."""
    
    def __init__(self):
        super().__init__(
            model=Credit,
            get_schema=CreditResponse,
            create_schema=CreditCreate,
            update_schema=CreditUpdate,
            list_schema=CreditList,
            not_found_message="Credit not found"
        )

