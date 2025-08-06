from fastapi import APIRouter
from api.domain.usecases.health.get_status import get_health_status_usecase   
from api.presentation.routes.router import DefaultRouter

router = APIRouter(route_class=DefaultRouter)

@router.get("/", summary="Verifica o status da API e leitura do CSV")
def health_check():
    """
    Verifica se o arquivo CSV está presente e pode ser carregado com sucesso.
    """
    return get_health_status_usecase()
