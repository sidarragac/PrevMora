import datetime
from typing import Optional

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, text
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Installment(Base):
    __tablename__ = "installment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    credit_id: Mapped[int] = mapped_column(ForeignKey("credit.id"), nullable=False)
    installments_number: Mapped[int] = mapped_column(Integer, nullable=False)
    due_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    installments_value: Mapped[Numeric] = mapped_column(Numeric, nullable=False)
    installment_state: Mapped[str] = mapped_column(String(50), nullable=False)
    payment_date: Mapped[Optional[datetime.date]] = mapped_column(Date, nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME2, nullable=False, server_default=text("GETDATE()")
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME2, nullable=False, server_default=text("GETDATE()")
    )
