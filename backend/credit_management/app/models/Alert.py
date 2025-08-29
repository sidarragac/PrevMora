from sqlalchemy import (
    Column, Integer, String, Date, Boolean, ForeignKey, DECIMAL, TIMESTAMP
)
from sqlalchemy.orm import relationship
from .base import Base

class Alert(Base):
    __tablename__ = "alert"

    id = Column(Integer, primary_key=True)
    credit_id = Column(Integer, ForeignKey("credit.id"), nullable=False)
    # This table can obtain the client id with the credit relationship
    # client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    alert_type_id = Column(Integer, ForeignKey("alert_type.id"), nullable=False)
    manually_generated = Column(Boolean, nullable=False)
    alert_date = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    credits = relationship("Credit", back_populates="alerts")
    # client = relationship("Client", back_populates="alerts")
    alert_type = relationship("Alert_Type", back_populates="alerts", uselist=False)

    def __repr__(self):
        return f"<Alert(id={self.id}, credit_id={self.credit_id}, alert_type_id={self.alert_type_id}, " \
           f"manually_generated={self.manually_generated}, " \
           f"alert_date={self.alert_date}, created_at={self.created_at}, updated_at={self.updated_at})>"