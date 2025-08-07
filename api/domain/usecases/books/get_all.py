from api.infra.repository.book_repository import get_books_list
from api.domain.models.book import Book

def get_all_books_usecase() -> list[Book]:
    """Get all books from the database."""
    return get_books_list()