from pydantic import BaseModel
from typing import Optional, List

class Book(BaseModel):
    id: str
    title: str
    price: float
    rating: int
    availability: str
    category: str
    image: Optional[str]

class BookListResponse(BaseModel):
    books: List[Book]