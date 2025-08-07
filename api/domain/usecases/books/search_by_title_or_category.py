from typing import Optional
from api.infra.repository.book_repository import BookRepository
from api.domain.models.book import Book


class SearchByTitleOrCategoryUseCase:
    """Use case for searching books by title and/or category."""
    
    def __init__(self, repository: BookRepository):
        self.repository = repository
    
    def execute(self, title: Optional[str] = None, category: Optional[str] = None) -> list[Book]:
        """Execute the use case to search books by title and/or category."""
        books = self.repository.get_books_list()

        if title and category:
            return [
                book for book in books 
                if title.lower() in book.title.lower() 
                and category.lower() in book.category.lower()
            ]
        elif title:
            return [
                book for book in books 
                if title.lower() in book.title.lower()
            ]
        elif category:
            return [
                book for book in books 
                if category.lower() in book.category.lower()
            ]

        return books