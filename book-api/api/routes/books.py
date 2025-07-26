from fastapi import APIRouter, HTTPException, Query
from api.core.database import get_books_list
from api.core.models.book import Book
from typing import List
from usecases.books.get_all import get_all_books_usecase
from usecases.books.get_by_id import get_book_by_id_usecase
from usecases.books.get_top_rated import get_top_rated_books_usecase
from usecases.books.get_by_title_or_category import search_by_title_or_category_usecase
from usecases.books.get_by_price import get_by_price_usecase

router = APIRouter()

@router.get("/", summary="Lista todos os livros", response_model=List[Book])
def list_books():
    """Retorna a lista completa de livros."""
    return get_all_books_usecase()

@router.get("/id/{book_id}", summary="Detalhes de um livro específico", response_model=Book)
def get_book(book_id: str):
    """Retorna detalhes de um livro pelo uuid."""
    book = get_book_by_id_usecase(book_id)
    if book:
        return book
    raise HTTPException(status_code=404, detail="Livro não encontrado.")

@router.get("/search", summary="Busca livros por título e/ou categoria", response_model=List[Book])
def search_books(title: str = "", category: str = ""):
    """
    Busca livros por título e/ou categoria.
    É possível passar apenas 'title' ou apenas 'category'.
    """
    return search_by_title_or_category_usecase(title, category)

@router.get("/top-rated", summary="Top livros com maior rating", response_model=List[Book])
def top_rated_books(limit: int = 0):
    """Retorna os livros com maior avaliação (rating). É possível limitar a quantidade retornada."""
    return get_top_rated_books_usecase(limit)

@router.get("/price-range", summary="Filtra livros por faixa de preço", response_model=List[Book])
def filter_by_price(min: float = Query(0), max: float = Query(1000)):
    """Filtra os livros por um intervalo de preço."""
    return get_by_price_usecase(min, max)
