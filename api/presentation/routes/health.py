from fastapi import APIRouter, Depends
from api.domain.repositories.book_repository import BookRepository
from api.domain.usecases.health.get_health_status import GetHealthStatusUseCase
from api.presentation.routes.router import DefaultRouter
from api.presentation.factories.repository_factory import build_book_repository

router = APIRouter(route_class=DefaultRouter)


@router.get("/", summary="Verifica o status da API e leitura do CSV")
def health_check(repository: BookRepository = Depends(build_book_repository)):
    """Verifica o status de saúde da aplicação."""
    use_case = GetHealthStatusUseCase(repository)
    return use_case.execute()
