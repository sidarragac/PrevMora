from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Client(Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    document: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    zone: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)

    credit: Mapped[list["Credit"]] = relationship("Credit", back_populates="client")
    alert: Mapped[list["Alert"]] = relationship("Alert", back_populates="client")

    def __repr__(self):
        return (
            f"<Client(id={self.id}, status={self.status}, name={self.name}, "
            f"document={self.document}, phone={self.phone}, email={self.email}, address={self.address}, zone={self.zone})>"
        )
