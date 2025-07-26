from fastapi import HTTPException
from api.core.database import get_books_dataframe
import pandas as pd

def get_categories_stats_usecase() -> list[dict]:
    df = get_books_dataframe()
    if "category" not in df.columns:
        raise HTTPException(status_code=500, detail="Coluna 'category' ausente.")
    
    grouped = df.groupby("category").agg(
        total_books=pd.NamedAgg(column="title", aggfunc="count"),
        avg_price=pd.NamedAgg(column="price", aggfunc="mean")
    ).reset_index()

    grouped["avg_price"] = grouped["avg_price"].round(2)
    return grouped.to_dict(orient="records")