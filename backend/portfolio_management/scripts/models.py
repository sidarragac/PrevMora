import datetime
from typing import Optional

from sqlalchemy import TIMESTAMP, Boolean, Date, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# this file was generated with the following comand
# sqlacodegen sqlite:///database.db > models.py


class Base(DeclarativeBase):
    pass


class AlertType(Base):
    __tablename__ = "alert_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    alert: Mapped[list["Alert"]] = relationship("Alert", back_populates="alert_type")


class Client(Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    document: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    zone: Mapped[Optional[str]] = mapped_column(String)

    credit: Mapped[list["Credit"]] = relationship("Credit", back_populates="client")


class ClientState(Base):
    __tablename__ = "client_state"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)


class ContactMethod(Base):
    __tablename__ = "contact_method"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    portfolio: Mapped[list["Portfolio"]] = relationship(
        "Portfolio", back_populates="contact_method"
    )


class ContactResult(Base):
    __tablename__ = "contact_result"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    portfolio: Mapped[list["Portfolio"]] = relationship(
        "Portfolio", back_populates="contact_result"
    )


class CreditState(Base):
    __tablename__ = "credit_state"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    credit: Mapped[list["Credit"]] = relationship(
        "Credit", back_populates="credit_state"
    )


class InstallmentState(Base):
    __tablename__ = "installment_state"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    installment: Mapped[list["Installment"]] = relationship(
        "Installment", back_populates="installment_state"
    )


class ManagerZone(Base):
    __tablename__ = "manager_zone"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    manager: Mapped[list["Manager"]] = relationship(
        "Manager", back_populates="manager_zone"
    )


class PaymentChannel(Base):
    __tablename__ = "payment_channel"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    reconciliation: Mapped[list["Reconciliation"]] = relationship(
        "Reconciliation", back_populates="payment_channel"
    )


class Credit(Base):
    __tablename__ = "credit"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"), nullable=False)
    credit_state_id: Mapped[int] = mapped_column(
        ForeignKey("credit_state.id"), nullable=False
    )
    disbursement_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    payment_reference: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    disbursement_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    interest_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    total_quotas: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    client: Mapped["Client"] = relationship("Client", back_populates="credit")
    credit_state: Mapped["CreditState"] = relationship(
        "CreditState", back_populates="credit"
    )
    alert: Mapped[list["Alert"]] = relationship("Alert", back_populates="credit")
    installment: Mapped[list["Installment"]] = relationship(
        "Installment", back_populates="credit"
    )
    reconciliation: Mapped[list["Reconciliation"]] = relationship(
        "Reconciliation", back_populates="credit"
    )


class Manager(Base):
    __tablename__ = "manager"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    manager_zone_id: Mapped[int] = mapped_column(
        ForeignKey("manager_zone.id"), nullable=False
    )

    manager_zone: Mapped["ManagerZone"] = relationship(
        "ManagerZone", back_populates="manager"
    )
    portfolio: Mapped[list["Portfolio"]] = relationship(
        "Portfolio", back_populates="manager"
    )


class Alert(Base):
    __tablename__ = "alert"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    credit_id: Mapped[int] = mapped_column(ForeignKey("credit.id"), nullable=False)
    alert_type_id: Mapped[int] = mapped_column(
        ForeignKey("alert_type.id"), nullable=False
    )
    manually_generated: Mapped[bool] = mapped_column(Boolean, nullable=False)
    alert_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False)

    alert_type: Mapped["AlertType"] = relationship("AlertType", back_populates="alert")
    credit: Mapped["Credit"] = relationship("Credit", back_populates="alert")


class Installment(Base):
    __tablename__ = "installment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    credit_id: Mapped[int] = mapped_column(ForeignKey("credit.id"), nullable=False)
    installment_state_id: Mapped[int] = mapped_column(
        ForeignKey("installment_state.id"), nullable=False
    )
    installment_number: Mapped[int] = mapped_column(Integer, nullable=False)
    installment_value: Mapped[int] = mapped_column(Integer, nullable=False)
    due_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    payment_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    credit: Mapped["Credit"] = relationship("Credit", back_populates="installment")
    installment_state: Mapped["InstallmentState"] = relationship(
        "InstallmentState", back_populates="installment"
    )
    portfolio: Mapped[list["Portfolio"]] = relationship(
        "Portfolio", back_populates="installment"
    )


class Reconciliation(Base):
    __tablename__ = "reconciliation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    payment_channel_id: Mapped[int] = mapped_column(
        ForeignKey("payment_channel.id"), nullable=False
    )
    payment_reference: Mapped[int] = mapped_column(
        ForeignKey("credit.payment_reference"), nullable=False
    )
    payment_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    transaction_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    observation: Mapped[Optional[str]] = mapped_column(String)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    payment_channel: Mapped["PaymentChannel"] = relationship(
        "PaymentChannel", back_populates="reconciliation"
    )
    credit: Mapped["Credit"] = relationship("Credit", back_populates="reconciliation")


class Portfolio(Base):
    __tablename__ = "portfolio"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    installment_id: Mapped[int] = mapped_column(
        ForeignKey("installment.id"), nullable=False
    )
    contact_method_id: Mapped[int] = mapped_column(
        ForeignKey("contact_method.id"), nullable=False
    )
    contact_result_id: Mapped[int] = mapped_column(
        ForeignKey("contact_result.id"), nullable=False
    )
    manager_id: Mapped[int] = mapped_column(ForeignKey("manager.id"), nullable=False)
    management_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    observation: Mapped[Optional[str]] = mapped_column(String)
    payment_promise_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    contact_method: Mapped["ContactMethod"] = relationship(
        "ContactMethod", back_populates="portfolio"
    )
    contact_result: Mapped["ContactResult"] = relationship(
        "ContactResult", back_populates="portfolio"
    )
    installment: Mapped["Installment"] = relationship(
        "Installment", back_populates="portfolio"
    )
    manager: Mapped["Manager"] = relationship("Manager", back_populates="portfolio")

    # Begin Cors dinamic configuration
    # @property
    # def allowed_origins(self) -> list[str]:
    #     if self.ENVIRONMENT == "local" or self.ENVIRONMENT == "development":
    #         return ["*"]
    #     else:
    #         origins_str = config("ALLOWED_ORIGINS", default="")
    #         if origins_str:
    #             return [origin.strip() for origin in origins_str.split(",")]
    #         else:
    #             raise ValueError("ALLOWED_ORIGINS is not set properly or empty in the environment variables.")

    # @property
    # def allowed_methods(self) -> list[str]:
    #     if self.ENVIRONMENT in ["local", "development"] or self.DEBUG:
    #         # Allow all on development
    #         return ["*"]
    #     else:
    #         return ["GET", "POST", "PUT", "DELETE", "OPTIONS"]

    # @property
    # def allowed_headers(self) -> list[str]:
    #     if self.ENVIRONMENT in ["local", "development"] or self.DEBUG:
    #         # Allow all headers on development
    #         return ["*"]
    #     else:
    #         # Change to specific headers for production
    #         return [
    #             "Authorization",
    #             "Content-Type",
    #             "X-Requested-With",
    #             "Accept",
    #             "Origin"
    #         ]

    # @property
    # def cors_config(self) -> dict:
    #     return {
    #         "allow_origins": self.allowed_origins,
    #         "allow_credentials": self.IS_ALLOWED_CREDENTIALS,
    #         "allow_methods": self.allowed_methods,
    #         "allow_headers": self.allowed_headers,
    #     }
    # IS_ALLOWED_CREDENTIALS: bool = config("IS_ALLOWED_CREDENTIALS", cast=bool)
