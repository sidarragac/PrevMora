import enum
import datetime
from typing import Optional
from sqlalchemy.dialects.mssql import DATETIME2

from sqlalchemy import (
    Integer, String, Date, Boolean, ForeignKey, Enum, text, BigInteger
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base
    
class PaymentChanelEnum(enum.Enum):
    OFFICE = "Oficina"
    CORRESPONDENT = "Corresponsal"
    TRANSFER = "Transferencia"
    BRANCH = "Sucursal"

class Reconciliation(Base):
    __tablename__ = 'reconciliation'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    payment_channel: Mapped[PaymentChanelEnum] = mapped_column(Enum(PaymentChanelEnum), nullable=False)
    payment_reference: Mapped[BigInteger] = mapped_column(ForeignKey('credit.payment_reference'), nullable=False)
    payment_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    transaction_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    observation: Mapped[Optional[str]] = mapped_column(String)
    
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

    credit: Mapped['Credit'] = relationship('Credit', back_populates='reconciliation')