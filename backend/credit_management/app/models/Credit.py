import datetime
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy import (
    Integer, Date, ForeignKey, text, String
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base

INTEREST_RATE_MULTIPLIER = 10000

class Credit(Base):
    __tablename__ = 'credit'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('client.id'), nullable=False)
    disbursement_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    disbursement_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    interest_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    total_quotas: Mapped[int] = mapped_column(Integer, nullable=False)
    credit_state: Mapped[str] = mapped_column(String(50), nullable=False)
    payment_reference: Mapped[str] = mapped_column(String(50), nullable=False)
    
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

    client: Mapped['Client'] = relationship('Client', back_populates='credit')
    alert: Mapped[list['Alert']] = relationship('Alert', back_populates='credit')
    installment: Mapped[list['Installment']] = relationship('Installment', back_populates='credit')

    def __repr__(self):
        return f"<Credit(id={self.id}, client_id={self.client_id}, credit_state={self.credit_state}, " \
           f"disbursement_amount={self.disbursement_amount}, payment_reference={self.payment_reference}, " \
           f"disbursement_date={self.disbursement_date}, interest_rate={self.interest_rate}, " \
           f"total_quotas={self.total_quotas})>"