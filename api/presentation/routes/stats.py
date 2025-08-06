from typing import List

from fastapi import APIRouter

from api.domain.models.stats import CategoryStats, StatsOverview
from api.domain.usecases.stats.get_categories import get_categories_stats_usecase
from api.domain.usecases.stats.get_overview import get_stats_overview_usecase
from api.presentation.routes.router import DefaultRouter

router = APIRouter(route_class=DefaultRouter)

@router.get("/overview", 
          summary="Estatísticas gerais dos livros", 
          response_model=StatsOverview)
def get_overview():
    """Retorna estatísticas gerais sobre os livros."""
    return get_stats_overview_usecase()

@router.get("/categories", 
          summary="Estatísticas por categoria", 
          response_model=List[CategoryStats])
def get_categories():
    """Retorna estatísticas agrupadas por categoria."""
    return get_categories_stats_usecase()
