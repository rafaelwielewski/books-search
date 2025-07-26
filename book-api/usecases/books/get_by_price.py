from fastapi.params import Query
from api.core.database import get_books_list

def get_by_price_usecase(min: float = Query(0), max: float = Query(1000)):
    """Filtra os livros por um intervalo de preço."""
    books = get_books_list()
    filtered = [b for b in books if min <= b["price"] <= max]
    return filtered