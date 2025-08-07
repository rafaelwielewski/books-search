from typing import List
from api.infra.repository.book_repository import get_books_list

def get_all_categories_usecase() -> List[str]:
    """Get all unique categories from books."""
    books = get_books_list()
    categories = []
    for book in books:
        if book.category not in categories:
            categories.append(book.category)
    return categories