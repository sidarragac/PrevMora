from sqlalchemy import (
    Column, Integer, String, Date, Boolean, ForeignKey, DECIMAL, TIMESTAMP
)
from sqlalchemy.orm import relationship
from .base import Base

class Credit(Base):
    __tablename__ = "credit"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    credit_state_id = Column(Integer, ForeignKey("credit_state.id"), nullable=False)
    disbursement_amount = Column(Integer, nullable=False)
    payment_reference = Column(Integer, unique=True, nullable=False)
    disbursement_date = Column(Date, nullable=False)
    interest_rate = Column(Integer, nullable=False)
    total_quotas = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    client = relationship("Client", back_populates="credits")
    credit_state = relationship("Credit_State", back_populates="credits")
    installments = relationship("Installment", back_populates="credit")
    alerts = relationship("Alert", back_populates="credits")
    reconciliations = relationship("Reconciliation", back_populates="credit", foreign_keys="[Reconciliation.payment_reference]")
    
    def __repr__(self):
        return f"<Credit(id={self.id}, client_id={self.client_id}, credit_state_id={self.credit_state_id}, " \
           f"disbursement_amount={self.disbursement_amount}, payment_reference={self.payment_reference}, " \
           f"disbursement_date={self.disbursement_date}, interest_rate={self.interest_rate}, " \
           f"total_quotas={self.total_quotas})>"