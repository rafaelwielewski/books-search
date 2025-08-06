import os

import pandas as pd
from fastapi import HTTPException


def get_books_dataframe() -> pd.DataFrame:
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


def get_books_list() -> list:
    """Get books data as a list of dictionaries."""
    df = get_books_dataframe()
    return df.to_dict('records')
