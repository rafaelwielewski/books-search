from typing import List

from fastapi import APIRouter, HTTPException, Query

from api.domain.models.book import Book
from api.domain.usecases.books.get_all import get_all_books_usecase
from api.domain.usecases.books.get_by_id import get_book_by_id_usecase
from api.domain.usecases.books.get_by_price import get_by_price_usecase
from api.domain.usecases.books.get_by_title_or_category import search_by_title_or_category_usecase
from api.domain.usecases.books.get_top_rated import get_top_rated_books_usecase
from api.presentation.routes.router import DefaultRouter

router = APIRouter(route_class=DefaultRouter)

@router.get("/", summary="Lista todos os livros", response_model=List[Book])
def list_books():
    """Lista todos os livros disponíveis."""
    return get_all_books_usecase()

@router.get("/top-rated", summary="Lista livros mais bem avaliados", response_model=List[Book])
def list_top_rated_books():
    """Lista os livros mais bem avaliados."""
    return get_top_rated_books_usecase()

@router.get("/search", summary="Busca livros por título ou categoria", response_model=List[Book])
def search_books(
    title: str = Query(None, description="Título do livro para busca"),
    category: str = Query(None, description="Categoria do livro para busca")
):
    """Busca livros por título ou categoria."""
    if not title and not category:
        raise HTTPException(
            status_code=400, 
            detail="Pelo menos um parâmetro de busca (title ou category) deve ser fornecido"
        )
    
    return search_by_title_or_category_usecase(title, category)

@router.get("/filter-by-price", summary="Filtra livros por faixa de preço", response_model=List[Book])
def filter_by_price(
    min_price: float = Query(None, description="Preço mínimo"),
    max_price: float = Query(None, description="Preço máximo")
):
    """Filtra livros por faixa de preço."""
    return get_by_price_usecase(min_price, max_price)

@router.get("/{book_id}", summary="Obtém um livro específico", response_model=Book)
def get_book(book_id: str):
    """Obtém um livro específico pelo ID."""
    book = get_book_by_id_usecase(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book
