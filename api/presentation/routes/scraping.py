from fastapi import APIRouter, Depends

from api.presentation.authorization.auth import get_current_user
from scripts.scrape_books import scrape
from api.presentation.routes.router import DefaultRouter


router = APIRouter(route_class=DefaultRouter)

@router.post("/trigger")
async def trigger_scraping(_user=Depends(get_current_user)):
    """Dispara o processo de scraping de livros."""
    result = scrape()
    return {"message": "Scraping iniciado", "result": result}