from api.infra.repository.book_repository import get_books_list
from api.domain.models.book import Book

def get_book_by_id_usecase(book_id: str) -> Book | None:
    """Get a book by its ID."""
    books = get_books_list()
    for book in books:
        if book.id == book_id:
            return book
    return None