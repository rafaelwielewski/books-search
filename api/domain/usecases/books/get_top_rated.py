from api.infra.repository.book_repository import get_books_list
from api.domain.models.book import Book

def get_top_rated_books_usecase(limit: int = 0) -> list[Book]:
    """Get top rated books with optional limit."""
    books = get_books_list()
    books_sorted = sorted(books, key=lambda x: x.rating, reverse=True)
    if limit > 0:
        return books_sorted[:limit]
    return books_sorted