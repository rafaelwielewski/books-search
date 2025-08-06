from pydantic import BaseModel

class StatsOverview(BaseModel):
    total_books: int
    average_price: float
    rating_distribution: dict

class StatsByCategory(BaseModel):
    category: str
    total_books: int
    avg_price: float