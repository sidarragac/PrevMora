from sqlalchemy import (
    Column, Integer, String, Date, Boolean, ForeignKey, DECIMAL, TIMESTAMP
)
from sqlalchemy.orm import relationship
from .base import Base

class Installment_State(Base):
    __tablename__ = "installment_state"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    installments = relationship("Installment", back_populates="installment_state")