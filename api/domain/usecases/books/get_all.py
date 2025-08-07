from api.infra.repository.book_repository import get_books_list

def get_all_books_usecase() -> list:
    """Get all books from the database."""
    return get_books_list()