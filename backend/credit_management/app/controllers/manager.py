from .base import BaseController
from ..models.Manager import Manager
from ..schemas.Manager import ManagerResponse, ManagerCreate, ManagerUpdate, ManagerList


class ManagerController(BaseController):
    """Controller for Manager operations."""
    
    def __init__(self):
        super().__init__(
            model=Manager,
            get_schema=ManagerResponse,
            create_schema=ManagerCreate,
            update_schema=ManagerUpdate,
            list_schema=ManagerList,
            not_found_message="Manager not found"
        )

