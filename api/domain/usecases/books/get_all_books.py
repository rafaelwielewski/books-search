from api.domain.repositories.book_repository import BookRepository
from api.domain.models.book import Book


class GetAllBooksUseCase:
    """Use case for getting all books."""
    
    def __init__(self, book_repository: BookRepository):
        self.repository = book_repository
    
    def execute(self) -> list[Book]:
        """Execute the use case to get all books."""
        return self.repository.get_books_list()