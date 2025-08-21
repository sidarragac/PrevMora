# from sqlalchemy import Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from pydantic import BaseModel

# Base = declarative_base()

# class Book(Base):
#     __tablename__ = "books"

#     id = Column(Integer, primary_key=True, index=True)
#     isbn = Column(String, unique=True, index=True)
#     title = Column(String, index=True)
#     author = Column(String, index=True)

# class BookCreate(BaseModel):
#     isbn: str
#     title: str
#     author: str

# class BookInDB(BookCreate):
#     id: int

# class BookUpdate(BookInDB):
#     title: str | None
#     author: str | None

# class BookResponse(BaseModel):
#     isbn: str
#     title: str
#     author: str