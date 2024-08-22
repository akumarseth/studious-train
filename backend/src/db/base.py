import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base for all models."""

    metadata = sa.MetaData()
