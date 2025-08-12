from typing import List

from fastapi import APIRouter, HTTPException, Query, Depends

from api.domain.models.book import Book
from api.infra.repository.book_repository import BookRepository
from api.domain.usecases.books.get_all_books import GetAllBooksUseCase
from api.domain.usecases.books.get_by_id_books import GetBookByIdUseCase
from api.domain.usecases.books.get_by_price_books import GetByPriceUseCase
from api.domain.usecases.books.search_by_title_or_category import SearchByTitleOrCategoryUseCase
from api.domain.usecases.books.get_top_rated_books import GetTopRatedBooksUseCase
from api.presentation.routes.router import DefaultRouter

router = APIRouter(route_class=DefaultRouter)


def get_book_repository() -> BookRepository:
    """Dependency to get book repository."""
    return BookRepository()


@router.get("/", summary="Lista todos os livros", response_model=List[Book])
def list_books(repository: BookRepository = Depends(get_book_repository)):
    """Lista todos os livros disponíveis."""
    use_case = GetAllBooksUseCase(repository)
    return use_case.execute()


@router.get("/top-rated", summary="Lista livros mais bem avaliados", response_model=List[Book])
def list_top_rated_books(repository: BookRepository = Depends(get_book_repository)):
    """Lista os livros mais bem avaliados."""
    use_case = GetTopRatedBooksUseCase(repository)
    return use_case.execute()


@router.get("/search", summary="Busca livros por título ou categoria", response_model=List[Book])
def search_books(
    title: str = Query(None, description="Título do livro para busca"),
    category: str = Query(None, description="Categoria do livro para busca"),
    repository: BookRepository = Depends(get_book_repository)
):
    """Busca livros por título ou categoria."""
    if not title and not category:
        raise HTTPException(
            status_code=400, 
            detail="Pelo menos um parâmetro de busca (title ou category) deve ser fornecido"
        )
    
    use_case = SearchByTitleOrCategoryUseCase(repository)
    return use_case.execute(title, category)


@router.get("/price-range", summary="Filtra livros por faixa de preço", response_model=List[Book])
def filter_by_price(
    min_price: float = Query(None, description="Preço mínimo"),
    max_price: float = Query(None, description="Preço máximo"),
    repository: BookRepository = Depends(get_book_repository)
):
    """Filtra livros por faixa de preço."""
    use_case = GetByPriceUseCase(repository)
    return use_case.execute(min_price, max_price)


@router.get("/{book_id}", summary="Obtém um livro específico", response_model=Book)
def get_book(book_id: str, repository: BookRepository = Depends(get_book_repository)):
    """Obtém um livro específico pelo ID."""
    use_case = GetBookByIdUseCase(repository)
    book = use_case.execute(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book
