from sqlalchemy import (
    Column, Integer, String, Date, Boolean, ForeignKey, DECIMAL, TIMESTAMP
)
from sqlalchemy.orm import relationship
from .base import Base

class Contact_Method(Base):
    __tablename__ = "contact_method"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    portfolios = relationship("Portfolio", back_populates="contact_method")


    def __repr__(self):
        return f"<Contact_Method(id={self.id}, name={self.name})>"