from sqlalchemy import (
    Column, Integer, String, Date, Boolean, ForeignKey, DECIMAL, TIMESTAMP
)
from sqlalchemy.orm import relationship
from .base import Base

class Client_State(Base):
    __tablename__ = "client_state"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    clients = relationship("Client", back_populates="client_state")