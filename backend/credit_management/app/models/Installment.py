from sqlalchemy import (
    Column, Integer, String, Date, Boolean, ForeignKey, DECIMAL, TIMESTAMP
)
from sqlalchemy.orm import relationship
from .base import Base

class Installment(Base):
    __tablename__ = "installment"

    id = Column(Integer, primary_key=True)
    credit_id = Column(Integer, ForeignKey("credit.id"), nullable=False)
    installment_state_id = Column(Integer, ForeignKey("installment_state.id"), nullable=False)
    installment_number = Column(Integer, nullable=False)
    installment_value = Column(Integer, nullable=False)
    due_date = Column(Date, nullable=False)
    payment_date = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    credit = relationship("Credit", back_populates="installments")
    installment_state = relationship("Installment_State", back_populates="installments")
    portfolios = relationship("Portfolio", back_populates="installment")

    def __repr__(self):
        return f"<Installment(id={self.id}, installment_number={self.installment_number}, due_date={self.due_date})>"