from api.infra.repository.book_repository import BookRepository
from api.domain.models.book import Book


class GetAllBooksUseCase:
    """Use case for getting all books."""
    
    def __init__(self, repository: BookRepository):
        self.repository = repository
    
    def execute(self) -> list[Book]:
        """Execute the use case to get all books."""
        return self.repository.get_books_list()