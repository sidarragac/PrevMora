from sqlalchemy import (
    Column, Integer, String, Date, Boolean, ForeignKey, DECIMAL, TIMESTAMP
)
from sqlalchemy.orm import relationship
from .base import Base

class Payment_Channel(Base):
    __tablename__ = "payment_channel"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    reconciliations = relationship("Reconciliation", back_populates="payment_channel")

    def __repr__(self):
        return f"<Payment_Channel(id={self.id}, name={self.name})>"