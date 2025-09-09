from .base import BaseController
from ..models.Alert import Alert
from ..schemas.Alert import AlertResponse, AlertCreate, AlertList


class AlertController(BaseController):
    """Controller for Alert operations."""
    
    def __init__(self):
        super().__init__(
            model=Alert,
            get_schema=AlertResponse,
            create_schema=AlertCreate,
            list_schema=AlertList,
            not_found_message="Alert not found"
        )

