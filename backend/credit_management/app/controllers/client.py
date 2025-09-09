from .base import BaseController
from ..models.Client import Client
from ..schemas.Client import ClientResponse, ClientCreate, ClientUpdate, ClientList


class ClientController(BaseController):
    """Controller for Client operations."""
    
    def __init__(self):
        super().__init__(
            model=Client,
            get_schema=ClientResponse,
            create_schema=ClientCreate,
            update_schema=ClientUpdate,
            list_schema=ClientList,
            not_found_message="Client not found"
        )

