from typing import List
from api.infra.repository.book_repository import BookRepository


class GetAllCategoriesUseCase:
    """Use case for getting all unique categories from books."""
    
    def __init__(self, book_repository: BookRepository):
        self.repository = book_repository
    
    def execute(self) -> List[str]:
        """Execute the use case to get all unique categories from books."""
        books = self.repository.get_books_list()
        categories = []
        for book in books:
            if book.category not in categories:
                categories.append(book.category)
        return categories