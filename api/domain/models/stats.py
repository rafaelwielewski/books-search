from pydantic import BaseModel


class StatsOverview(BaseModel):
    total_books: int
    average_price: float
    average_rating: float


class CategoryStats(BaseModel):
    category: str
    count: int