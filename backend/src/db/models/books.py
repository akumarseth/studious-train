from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from src.db.base import Base

class Book(Base):
    __tablename__ = "books"
    __table_args__ = {"schema": "jktech"}  # Specify the schema

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    genre = Column(String)
    year_published = Column(Integer)
    summary = Column(Text)

    reviews = relationship("Review", back_populates="book", cascade="all, delete")