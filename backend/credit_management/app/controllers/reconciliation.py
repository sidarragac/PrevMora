from .base import BaseController
from ..models.Reconciliation import Reconciliation
from ..schemas.Reconciliation import ReconciliationResponse, ReconciliationCreate, ReconciliationList


class ReconciliationController(BaseController):
    """Controller for Reconciliation operations."""
    
    def __init__(self):
        super().__init__(
            model=Reconciliation,
            get_schema=ReconciliationResponse,
            create_schema=ReconciliationCreate,
            list_schema=ReconciliationList,
            not_found_message="Reconciliation not found"
        )

