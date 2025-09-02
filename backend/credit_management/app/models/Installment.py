import enum
import datetime
from typing import Optional
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy import (
    Integer,Date, ForeignKey, Enum, text
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base

class InstallmentStateEnum(enum.Enum):
    PAID = "Pagada"
    PENDING = "Pendiente"
    PROMISE = "Promesa de pago"
    OVERDUE = "Vencida"

class Installment(Base):
    __tablename__ = 'installment'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    credit_id: Mapped[int] = mapped_column(ForeignKey('credit.id'), nullable=False)
    installment_state: Mapped[InstallmentStateEnum] = mapped_column(Enum(InstallmentStateEnum), nullable=False)
    installment_number: Mapped[int] = mapped_column(Integer, nullable=False)
    installment_value: Mapped[int] = mapped_column(Integer, nullable=False)
    due_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    payment_date: Mapped[Optional[datetime.date]] = mapped_column(Date, nullable=True)
    
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

    credit: Mapped['Credit'] = relationship('Credit', back_populates='installment')
    portfolio: Mapped[list['Portfolio']] = relationship('Portfolio', back_populates='installment')

    def __repr__(self):
        return f"<Installment(id={self.id}, installment_number={self.installment_number}, due_date={self.due_date})>"