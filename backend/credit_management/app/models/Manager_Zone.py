from sqlalchemy import (
    Column, Integer, String, Date, Boolean, ForeignKey, DECIMAL, TIMESTAMP
)
from sqlalchemy.orm import relationship
from .base import Base
    
class Manager_Zone(Base):
    __tablename__ = "manager_zone"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    managers = relationship("Manager", back_populates="manager_zone")

    def __repr__(self):
        return f"<Manager_Zone(id={self.id}, name={self.name})>"