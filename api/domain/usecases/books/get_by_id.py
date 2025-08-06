from api.infra.database import get_books_list

def get_book_by_id_usecase(book_id: str) -> dict | None:
    """Get a book by its ID."""
    books = get_books_list()
    for book in books:
        if book["id"] == book_id:
            return book
    return None