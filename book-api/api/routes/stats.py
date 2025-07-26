from fastapi import APIRouter
from api.core.models.stats import StatsOverview, StatsByCategory
from typing import List
from usecases.stats.get_overview import get_stats_overview_usecase
from usecases.stats.get_categories import get_categories_stats_usecase
from api.routes.router import DefaultRouter

router = APIRouter(route_class=DefaultRouter)

@router.get("/overview", summary="Estatísticas gerais da coleção de livros", response_model=StatsOverview)
def stats_overview():
    """Retorna uma visão geral das estatísticas da coleção de livros."""
    return get_stats_overview_usecase()

@router.get("/categories", summary="Estatísticas por categoria", response_model=List[StatsByCategory])
def stats_by_category():
    """Retorna estatísticas detalhadas por categoria de livros."""
    return get_categories_stats_usecase()
