from typing import Optional
from api.infra.repository.book_repository import get_books_list

def get_by_price_usecase(min_price: Optional[float] = None, max_price: Optional[float] = None) -> list:
    """Filter books by price range."""
    books = get_books_list()
    filtered_books = []
    
    for book in books:
        if min_price is not None and book['price'] < min_price:
            continue
        if max_price is not None and book['price'] > max_price:
            continue
        filtered_books.append(book)
    
    return filtered_books