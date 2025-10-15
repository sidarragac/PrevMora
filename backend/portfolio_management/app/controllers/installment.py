from ..models.Installment import Installment
from ..schemas.Installment import (
    InstallmentCreate,
    InstallmentList,
    InstallmentResponse,
)
from .base import BaseController


class InstallmentController(BaseController):
    """Controller for Installment operations."""

    def __init__(self):
        super().__init__(
            model=Installment,
            get_schema=InstallmentResponse,
            create_schema=InstallmentCreate,
            list_schema=InstallmentList,
            not_found_message="Installment not found",
        )
