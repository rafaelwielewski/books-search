from api.infra.repositories.book_repository_impl import BookRepositoryImpl
from api.domain.repositories.book_repository import BookRepository


def build_book_repository() -> BookRepository:
    """Factory function to create a BookRepository instance."""
    return BookRepositoryImpl() 