from typing import Optional
from api.infra.repository.book_repository import BookRepository
from api.domain.models.book import Book


class GetByPriceUseCase:
    """Use case for filtering books by price range."""
    
    def __init__(self, book_repository: BookRepository):
        self.repository = book_repository
    
    def execute(self, min_price: Optional[float] = None, max_price: Optional[float] = None) -> list[Book]:
        """Execute the use case to filter books by price range."""
        books = self.repository.get_books_list()
        filtered_books = []
        
        for book in books:
            if min_price is not None and book.price < min_price:
                continue
            if max_price is not None and book.price > max_price:
                continue
            filtered_books.append(book)
        
        return filtered_books