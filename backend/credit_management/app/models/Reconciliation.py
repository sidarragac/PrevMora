from sqlalchemy import (
    Column, Integer, String, Date, Boolean, ForeignKey, DECIMAL, TIMESTAMP
)
from sqlalchemy.orm import relationship
from .base import Base

class Reconciliation(Base):
    __tablename__ = "reconciliation"

    id = Column(Integer, primary_key=True)
    payment_channel_id = Column(Integer, ForeignKey("payment_channel.id"), nullable=False)
    payment_reference = Column(Integer, ForeignKey("credit.payment_reference"), nullable=False)
    payment_amount = Column(Integer, nullable=False)
    transaction_date = Column(Date, nullable=False)
    observation = Column(String, nullable=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    payment_channel = relationship("Payment_Channel", back_populates="reconciliations")
    credit = relationship("Credit", back_populates="reconciliations", foreign_keys=[payment_reference])

    def __repr__(self):
        return f"<Reconciliation(id={self.id}, payment_amount={self.payment_amount}, transaction_date={self.transaction_date})>"