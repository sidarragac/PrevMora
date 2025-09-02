import enum
import datetime
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy import (
    Integer, Date, ForeignKey, Enum, text, BigInteger
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base

class CreditStateEnum(enum.Enum):
    PENDING = "Pendiente"
    APPROVED = "Vigente"
    CANCELED = "Cancelado"
    MORA = "En Mora"

class Credit(Base):
    __tablename__ = 'credit'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('client.id'), nullable=False)
    credit_state: Mapped[CreditStateEnum] = mapped_column(Enum(CreditStateEnum), nullable=False)
    disbursement_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    payment_reference: Mapped[BigInteger] = mapped_column(BigInteger, nullable=False, unique=True)
    disbursement_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    interest_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    total_quotas: Mapped[int] = mapped_column(Integer, nullable=False)
    
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
    reconciliation: Mapped[list['Reconciliation']] = relationship('Reconciliation', back_populates='credit')

    def __repr__(self):
        return f"<Credit(id={self.id}, client_id={self.client_id}, credit_state={self.credit_state.value}, " \
           f"disbursement_amount={self.disbursement_amount}, payment_reference={self.payment_reference}, " \
           f"disbursement_date={self.disbursement_date}, interest_rate={self.interest_rate}, " \
           f"total_quotas={self.total_quotas})>"