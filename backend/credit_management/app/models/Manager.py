import enum
from sqlalchemy import (
    Integer, String, Enum
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base

class ManagerZoneEnum(enum.Enum):
    RURAL = "Rural"
    URBAN = "Urbano"

class Manager(Base):
    __tablename__ = 'manager'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    # I think that the document is necesary for the manager
    # document: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    manager_zone: Mapped[ManagerZoneEnum] = mapped_column(Enum(ManagerZoneEnum), nullable=False)

    portfolio: Mapped[list['Portfolio']] = relationship('Portfolio', back_populates='manager')

    def __repr__(self):
            return f"<Manager(id={self.id}, name={self.name}, manager_zone_id={self.manager_zone_id})>"