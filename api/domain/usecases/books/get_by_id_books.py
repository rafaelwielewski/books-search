from api.infra.repository.book_repository import BookRepository
from api.domain.models.book import Book


class GetBookByIdUseCase:
    """Use case for getting a book by its ID."""
    
    def __init__(self, repository: BookRepository):
        self.repository = repository
    
    def execute(self, book_id: str) -> Book | None:
        """Execute the use case to get a book by its ID."""
        books = self.repository.get_books_list()
        for book in books:
            if book.id == book_id:
                return book
        return None