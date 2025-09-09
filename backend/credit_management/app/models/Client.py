import enum
from typing import Optional
from sqlalchemy import (
    Integer, String, Enum
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base

class ClientStateEnum(enum.Enum):
    ACTIVE = "Activo"
    PUNISHED = "Castigado"
    OVERDUE = "En Mora"
    INACTIVE = "Inactivo"

class Client(Base):
    __tablename__ = 'client'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_state: Mapped[ClientStateEnum] = mapped_column(Enum(ClientStateEnum), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    document: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String, nullable=False)
    zone: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    credit: Mapped[list['Credit']] = relationship('Credit', back_populates='client')

    def __repr__(self):
        return f"<Client(id={self.id}, client_state={self.client_state}, name={self.name}, " \
           f"document={self.document}, phone={self.phone}, email={self.email}, address={self.address}, zone={self.zone})>"
