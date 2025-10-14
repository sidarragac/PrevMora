from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Manager(Base):
    __tablename__ = "manager"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    # I think that the document is necesary for the manager
    # document: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    manager_zone: Mapped[str] = mapped_column(String(50), nullable=False)

    portfolio: Mapped[list["Portfolio"]] = relationship(
        "Portfolio", back_populates="manager"
    )

    def __repr__(self):
        return f"<Manager(id={self.id}, name={self.name}, manager_zone={self.manager_zone})>"
