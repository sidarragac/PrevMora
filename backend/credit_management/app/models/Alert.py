import enum
import datetime
from typing import Optional
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy import (
    Integer, Date, Boolean, ForeignKey, Enum, text
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base

class AlertTypeEnum(enum.Enum):
    NO_ANSWER = "No respuesta"
    WARNING = "Riesgo de mora"
    VISIT_REQUIRED = "Requiere visita"

class Alert(Base):
    __tablename__ = 'alert'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    credit_id: Mapped[int] = mapped_column(ForeignKey('credit.id'), nullable=False)
    alert_type: Mapped[AlertTypeEnum] = mapped_column(Enum(AlertTypeEnum), nullable=False)
    manually_generated: Mapped[bool] = mapped_column(Boolean, nullable=False)
    alert_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    
    created_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME2, 
        nullable=False, 
        server_default=text('GETDATE()')
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME2, 
        nullable=False, 
        server_default=text('GETDATE()')
    )

    credit: Mapped['Credit'] = relationship('Credit', back_populates='alert')

    """
        This table can obtain the client id with the credit relationship, this is a change
        respect to the model, the deleted code is:
            client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
            client = relationship("Client", back_populates="alerts")
    """

    def __repr__(self):
        return f"<Alert(id={self.id}, credit_id={self.credit_id}, alert_type={self.alert_type.value}, " \
           f"manually_generated={self.manually_generated}, " \
           f"alert_date={self.alert_date}, created_at={self.created_at}, updated_at={self.updated_at})>"