from sqlalchemy import (
    Column, Integer, String, Date, Boolean, ForeignKey, DECIMAL, TIMESTAMP
)
from sqlalchemy.orm import relationship
from .base import Base

class Contact_Result(Base):
    __tablename__ = "contact_result"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    portfolios = relationship("Portfolio", back_populates="contact_result")