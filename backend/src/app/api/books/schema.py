from pydantic import BaseModel
from typing import List, Optional

class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: Optional[str] = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True


class BookContentRequest(BaseModel):
    content: str
