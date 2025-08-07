from fastapi import APIRouter, Depends
from api.infra.repository.book_repository import BookRepository
from api.domain.usecases.health.get_health_status import GetHealthStatusUseCase
from api.presentation.routes.router import DefaultRouter

router = APIRouter(route_class=DefaultRouter)


def get_book_repository() -> BookRepository:
    """Dependency to get book repository."""
    return BookRepository()


@router.get("/", summary="Verifica o status da API e leitura do CSV")
def health_check(repository: BookRepository = Depends(get_book_repository)):
    """Verifica o status de saúde da aplicação."""
    use_case = GetHealthStatusUseCase(repository)
    return use_case.execute()
