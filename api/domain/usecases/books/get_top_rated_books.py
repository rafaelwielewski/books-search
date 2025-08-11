from api.infra.repository.book_repository import BookRepository
from api.domain.models.book import Book


class GetTopRatedBooksUseCase:
    """Use case for getting top rated books."""
    
    def __init__(self, book_repository: BookRepository):
        self.repository = book_repository
    
    def execute(self, limit: int = 0) -> list[Book]:
        """Execute the use case to get top rated books with optional limit."""
        books = self.repository.get_books_list()
        books_sorted = sorted(books, key=lambda x: x.rating, reverse=True)
        if limit > 0:
            return books_sorted[:limit]
        return books_sorted