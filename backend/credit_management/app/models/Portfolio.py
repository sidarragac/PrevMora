import enum
import datetime
from typing import Optional
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy import (
    Integer, String, Date, ForeignKey, DATETIME, Enum
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base

class ContactResultEnum(enum.Enum):
    SUCCESFUL = "Efectiva"
    NO_ANSWER = "Sin respuesta"
    BAD_CONTACT_INFORMATION = "Numero errado"
    PROMISE_TO_PAY = "Promesa de pago"

class ContactMethodEnum(enum.Enum):
    PHONE = "Telefono"
    EMAIL = "Correo"
    WHATSAPP = "WhatsApp"
    VISIT = "Visita"

class Portfolio(Base):
    __tablename__ = 'portfolio'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    installment_id: Mapped[int] = mapped_column(ForeignKey('installment.id'), nullable=False)
    manager_id: Mapped[int] = mapped_column(ForeignKey('manager.id'), nullable=False)
    contact_method: Mapped[ContactMethodEnum] = mapped_column(Enum(ContactMethodEnum), nullable=False)
    contact_result: Mapped[ContactResultEnum] = mapped_column(Enum(ContactResultEnum), nullable=False)
    management_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    observation: Mapped[Optional[str]] = mapped_column(String)
    payment_promise_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME)

    installment: Mapped['Installment'] = relationship('Installment', back_populates='portfolio')
    manager: Mapped['Manager'] = relationship('Manager', back_populates='portfolio')

    def __repr__(self):
        return f"<Portfolio(id={self.id}, management_date={self.management_date}, observation={self.observation})>"