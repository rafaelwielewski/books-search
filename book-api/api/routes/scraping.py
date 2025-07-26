from fastapi import APIRouter, Depends
from api.core.auth import get_current_user
from scripts.scrape_books import scrape
from api.routes.router import DefaultRouter

router = APIRouter(route_class=DefaultRouter)

@router.post("/trigger", summary="Dispara a atualização do catálogo de livros")
def trigger_scraping(user: str = Depends(get_current_user)):
    """
    Executa o processo de scraping para atualizar o catálogo de livros.
    Faz a raspagem de dados do site books.toscrape.com e salva os resultados em um arquivo CSV.
    """
    return scrape()