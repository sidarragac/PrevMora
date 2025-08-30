from sqlalchemy import (
    Column, Integer, String, Date, Boolean, ForeignKey, DECIMAL, TIMESTAMP
)
from sqlalchemy.orm import relationship
from .base import Base

class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True)
    client_state = Column(Integer, ForeignKey("client_state.id"), nullable=False)
    name = Column(String, nullable=False)
    document = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String, nullable=False)
    zone = Column(String, nullable=True)

    client_state = relationship("Client_State", back_populates="clients")
    credits = relationship("Credit", back_populates="client")
    # For more information about this comment go to the file Alert.py
    # alerts = relationship("Alert", back_populates="client")

    def __repr__(self):
        return f"<Client(id={self.id}, client_state={self.client_state}, name={self.name}, " \
           f"document={self.document}, phone={self.phone}, email={self.email}, address={self.address}, zone={self.zone})>"