import pandas as pd
import os
from fastapi import HTTPException

DATA_PATH = "data/books.csv"

def get_books_dataframe():
    """Carrega o dataframe de livros do CSV."""
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=500, detail="Arquivo CSV não encontrado.")
    
    try:
        df = pd.read_csv(DATA_PATH)
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar CSV: {str(e)}")

def get_books_list():
    """Retorna lista de livros como dicionários."""
    df = get_books_dataframe()
    return df.to_dict(orient="records")
