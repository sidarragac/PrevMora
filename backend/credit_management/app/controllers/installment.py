from .base import BaseController
from ..models.Installment import Installment
from ..schemas.Installment import InstallmentResponse, InstallmentCreate, InstallmentList


class InstallmentController(BaseController):
    """Controller for Installment operations."""
    
    def __init__(self):
        super().__init__(
            model=Installment,
            get_schema=InstallmentResponse,
            create_schema=InstallmentCreate,
            list_schema=InstallmentList,
            not_found_message="Installment not found"
        )

