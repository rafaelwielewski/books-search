import os

import pandas as pd
from fastapi import HTTPException

from api.domain.models.book import Book


def _get_books_dataframe() -> pd.DataFrame:
    """Load books data from CSV file."""
    csv_path = os.path.join("data", "books.csv")
    
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=500, detail="Arquivo de dados não encontrado")
    
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f'Erro ao carregar CSV: {str(e)}'
        ) from e


def get_books_list() -> list[Book]:
    """Get books data as a list of Book models."""
    df = _get_books_dataframe()
    books = []
    
    for _, row in df.iterrows():
        book_data = {
            'id': str(row.get('id', '')),
            'title': str(row.get('title', '')),
            'category': str(row.get('category', '')),
            'price': float(row.get('price', 0.0)),
            'rating': float(row.get('rating', 0.0)),
            'image': str(row.get('image', '')) if pd.notna(row.get('image')) else None
        }
        books.append(Book(**book_data))
    
    return books
