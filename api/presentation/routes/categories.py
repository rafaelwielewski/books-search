from fastapi import APIRouter, Depends
from api.infra.repository.book_repository import BookRepository
from api.domain.usecases.categories.get_all_categories import GetAllCategoriesUseCase
from api.presentation.routes.router import DefaultRouter

router = APIRouter(route_class=DefaultRouter)


def get_book_repository() -> BookRepository:
    """Dependency to get book repository."""
    return BookRepository()


@router.get("/", summary="Lista todas as categorias de livros disponíveis")
def get_all_categories(repository: BookRepository = Depends(get_book_repository)):
    """Retorna uma lista de todas as categorias de livros disponíveis."""
    use_case = GetAllCategoriesUseCase(repository)
    return use_case.execute()
