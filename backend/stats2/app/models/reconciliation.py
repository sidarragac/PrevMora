import datetime
from typing import Optional

from sqlalchemy import Date, Integer, String, text
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Reconciliation(Base):
    __tablename__ = "reconciliation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transaction_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    payment_reference: Mapped[str] = mapped_column(String(50), nullable=False)
    payment_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    payment_channel: Mapped[str] = mapped_column(String(50), nullable=False)
    observation: Mapped[Optional[str]] = mapped_column(String(500))

    created_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME2, nullable=False, server_default=text("GETDATE()")
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME2, nullable=False, server_default=text("GETDATE()")
    )