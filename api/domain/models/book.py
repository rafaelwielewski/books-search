from typing import List, Optional

from pydantic import BaseModel


class Book(BaseModel):
    id: str
    title: str
    category: str
    price: float
    rating: float
    availability: str
    image: Optional[str] = None

class BookListResponse(BaseModel):
    books: List[Book]