from typing import Optional
from api.infra.database import get_books_list

def search_by_title_or_category_usecase(
    title: Optional[str] = None, 
    category: Optional[str] = None
) -> list:
    """Search books by title and/or category."""
    books = get_books_list()

    if title and category:
        return [
            book for book in books 
            if title.lower() in book['title'].lower() 
            and category.lower() in book['category'].lower()
        ]
    elif title:
        return [
            book for book in books 
            if title.lower() in book['title'].lower()
        ]
    elif category:
        return [
            book for book in books 
            if category.lower() in book['category'].lower()
        ]

    return books