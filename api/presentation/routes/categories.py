from fastapi import APIRouter, Depends
from api.domain.repositories.book_repository import BookRepository
from api.domain.usecases.categories.get_all_categories import GetAllCategoriesUseCase
from api.presentation.routes.router import DefaultRouter
from api.presentation.factories.repository_factory import build_book_repository

router = APIRouter(route_class=DefaultRouter)


@router.get("/", summary="Lista todas as categorias de livros disponíveis")
def get_all_categories(repository: BookRepository = Depends(build_book_repository)):
    """Retorna uma lista de todas as categorias de livros disponíveis."""
    use_case = GetAllCategoriesUseCase(repository)
    return use_case.execute()
