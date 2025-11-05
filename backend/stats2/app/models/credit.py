import datetime

from sqlalchemy import Date, ForeignKey, Integer, String, text
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Credit(Base):
    __tablename__ = "credit"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"), nullable=False)
    disbursement_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    disbursement_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    interest_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    total_quotas: Mapped[int] = mapped_column(Integer, nullable=False)
    credit_state: Mapped[str] = mapped_column(String(50), nullable=False)
    payment_reference: Mapped[str] = mapped_column(String(50), nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME2, nullable=False, server_default=text("GETDATE()")
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME2, nullable=False, server_default=text("GETDATE()")
    )
