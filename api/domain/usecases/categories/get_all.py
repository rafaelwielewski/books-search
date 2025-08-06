from fastapi import HTTPException
from api.infra.database import get_books_dataframe

def get_all_categories_usecase() -> list[dict]:
    df = get_books_dataframe()
    
    if "category" not in df.columns:
        raise HTTPException(status_code=500, detail="Coluna 'category' ausente no CSV.")
    
    categories = df["category"].dropna().unique().tolist()
    return {"categories": sorted(categories)}