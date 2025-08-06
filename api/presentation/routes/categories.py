from fastapi import APIRouter
from api.domain.usecases.categories.get_all import get_all_categories_usecase
from api.presentation.routes.router import DefaultRouter

router = APIRouter(route_class=DefaultRouter)

@router.get("/", summary="Lista todas as categorias de livros disponíveis")
def get_all_categories():
    """Retorna uma lista de todas as categorias de livros disponíveis."""
    return get_all_categories_usecase()
