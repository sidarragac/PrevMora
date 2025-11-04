from .base import Base  # re-export Base

# Import models to ensure SQLAlchemy sees all mappers during configuration
from .client import Client  # noqa: F401
from .credit import Credit  # noqa: F401
from .installment import Installment  # noqa: F401
from .manager import Manager  # noqa: F401
from .portafolio import Portfolio  # noqa: F401
from .reconciliation import Reconciliation  # noqa: F401

__all__ = [
    "Base",
    "Client",
    "Credit",
    "Installment",
    "Manager",
    "Portfolio",
    "Reconciliation",
]
