from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from src.db.base import Base


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = {"schema": "jktech"}  # Specify the schema

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("jktech.books.id"))
    user_id = Column(Integer)
    review_text = Column(Text)
    rating = Column(Integer)

    book = relationship("Book", back_populates="reviews")

