import datetime

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, text
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Alert(Base):
    __tablename__ = "alert"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    credit_id: Mapped[int] = mapped_column(ForeignKey("credit.id"), nullable=False)
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"), nullable=False)
    alert_type: Mapped[str] = mapped_column(String(50), nullable=False)
    manually_generated: Mapped[bool] = mapped_column(Boolean, nullable=False)
    alert_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME2, nullable=False, server_default=text("GETDATE()")
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME2, nullable=False, server_default=text("GETDATE()")
    )
