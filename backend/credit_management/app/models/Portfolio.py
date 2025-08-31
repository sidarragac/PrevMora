from sqlalchemy import (
    Column, Integer, String, Date, Boolean, ForeignKey, DECIMAL, TIMESTAMP
)
from sqlalchemy.orm import relationship
from .base import Base

class Portfolio(Base):
    __tablename__ = "portfolio"

    id = Column(Integer, primary_key=True)
    installment_id = Column(Integer, ForeignKey("installment.id"), nullable=False)
    contact_method_id = Column(Integer, ForeignKey("contact_method.id"), nullable=False)
    contact_result_id = Column(Integer, ForeignKey("contact_result.id"), nullable=False)
    manager_id = Column(Integer, ForeignKey("manager.id"), nullable=False)
    management_date = Column(Date, nullable=False)
    observation = Column(String(255), nullable=True)
    payment_promise_date = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    
    installment = relationship("Installment", back_populates="portfolios")
    manager = relationship("Manager", back_populates="portfolios")
    contact_method = relationship("Contact_Method", back_populates="portfolios")
    contact_result = relationship("Contact_Result", back_populates="portfolios")

    def __repr__(self):
        return f"<Portfolio(id={self.id}, management_date={self.management_date}, observation={self.observation})>"