from typing import List

from fastapi import APIRouter, Depends

from api.domain.models.stats import CategoryStats, StatsOverview
from api.infra.repository.book_repository import BookRepository
from api.domain.usecases.stats.get_categories_stats import GetCategoriesStatsUseCase
from api.domain.usecases.stats.get_overview_stats import GetStatsOverviewUseCase
from api.presentation.routes.router import DefaultRouter

router = APIRouter(route_class=DefaultRouter)


def get_book_repository() -> BookRepository:
    """Dependency to get book repository."""
    return BookRepository()


@router.get("/overview", 
          summary="Estatísticas gerais dos livros", 
          response_model=StatsOverview)
def get_overview(repository: BookRepository = Depends(get_book_repository)):
    """Retorna estatísticas gerais sobre os livros."""
    use_case = GetStatsOverviewUseCase(repository)
    return use_case.execute()


@router.get("/categories", 
          summary="Estatísticas por categoria", 
          response_model=List[CategoryStats])
def get_categories(repository: BookRepository = Depends(get_book_repository)):
    """Retorna estatísticas agrupadas por categoria."""
    use_case = GetCategoriesStatsUseCase(repository)
    return use_case.execute()
