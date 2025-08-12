from abc import ABC, abstractmethod
from typing import List

from api.domain.models.book import Book


class BookRepository(ABC):
    """Interface for book repository operations."""
    
    @abstractmethod
    def get_books_list(self) -> List[Book]:
        """Get books data as a list of Book models."""
        pass 