import datetime
from typing import Optional

from sqlalchemy import Date, ForeignKey, Integer, String, text
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Portfolio(Base):
    __tablename__ = "portfolio"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    installment_id: Mapped[int] = mapped_column(
        ForeignKey("installment.id"), nullable=False
    )
    management_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    contact_method: Mapped[str] = mapped_column(String(50), nullable=False)
    contact_result: Mapped[str] = mapped_column(String(50), nullable=False)
    observation: Mapped[Optional[str]] = mapped_column(String(500))
    payment_promise_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    manager_id: Mapped[int] = mapped_column(ForeignKey("manager.id"), nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME2, nullable=False, server_default=text("GETDATE()")
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME2, nullable=False, server_default=text("GETDATE()")
    )

    installment: Mapped["Installment"] = relationship(
        "Installment", back_populates="portfolio"
    )
    manager: Mapped["Manager"] = relationship("Manager", back_populates="portfolio")

    def __repr__(self):
        return f"<Portfolio(id={self.id}, management_date={self.management_date}, observation={self.observation})>"