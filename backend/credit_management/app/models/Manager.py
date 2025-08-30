from sqlalchemy import (
    Column, Integer, String, Date, Boolean, ForeignKey, DECIMAL, TIMESTAMP
)
from sqlalchemy.orm import relationship
from .base import Base

# Is necesary document for manager?
class Manager(Base):
    __tablename__ = "manager"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    manager_zone_id = Column(Integer, ForeignKey("manager_zone.id"), nullable=False)

    manager_zone = relationship("Manager_Zone", back_populates="managers")
    portfolios = relationship("Portfolio", back_populates="manager")

    def __repr__(self):
        return f"<Manager(id={self.id}, name={self.name}, manager_zone_id={self.manager_zone_id})>"