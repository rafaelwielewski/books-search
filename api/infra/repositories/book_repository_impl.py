import os

import pandas as pd
from fastapi import HTTPException

from api.domain.models.book import Book
from api.domain.repositories.book_repository import BookRepository


class BookRepositoryImpl(BookRepository):
    """Repository implementation for book data operations."""
    
    def __init__(self):
        self.csv_path = os.path.join("data", "books.csv")
        
    def _to_model(self, row: pd.Series) -> Book:
        return Book(
            id=str(row.get('id', '')),
            title=str(row.get('title', '')),
            category=str(row.get('category', '')),
            price=float(row.get('price', 0.0)),
            rating=float(row.get('rating', 0.0)),
            availability=str(row.get('availability', '')),
            image=str(row.get('image', '')) if pd.notna(row.get('image')) else None
        )   
    
    def _get_books_dataframe(self) -> pd.DataFrame:
        """Load books data from CSV file."""
        if not os.path.exists(self.csv_path):
            raise HTTPException(status_code=500, detail="Arquivo de dados não encontrado")
        
        try:
            df = pd.read_csv(self.csv_path)
            return df
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f'Erro ao carregar CSV: {str(e)}'
            ) from e
    
    def get_books_list(self) -> list[Book]:
        """Get books data as a list of Book models."""
        df = self._get_books_dataframe()
        books = []
        
        for _, row in df.iterrows():
            books.append(self._to_model(row))
        
        return books
