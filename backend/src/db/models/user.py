from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.db.base import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "jktech"}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())
    last_login_time = Column(DateTime(timezone=True), onupdate=func.now())
