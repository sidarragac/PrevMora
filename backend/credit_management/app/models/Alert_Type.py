from sqlalchemy import (
    Column, Integer, String, Date, Boolean, ForeignKey, DECIMAL, TIMESTAMP
)
from sqlalchemy.orm import relationship
from .base import Base

class Alert_Type(Base):
    __tablename__ = "alert_type"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    alerts = relationship("Alert", back_populates="alert_type")

    def __repr__(self):
        return f"<Alert_Type(id={self.id}, name={self.name})>"