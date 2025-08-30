from sqlalchemy import (
    Column, Integer, String, Date, Boolean, ForeignKey, DECIMAL, TIMESTAMP
)
from sqlalchemy.orm import relationship
from .base import Base

class Credit_State(Base):
    __tablename__ = "credit_state"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    credits = relationship("Credit", back_populates="credit_state")

    def __repr__(self):
        return f"<Credit_State(id={self.id}, name={self.name})>"