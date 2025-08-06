from api.infra.database import get_books_dataframe

def get_stats_overview_usecase():
    """Get overview statistics of all books."""
    df = get_books_dataframe()
    
    return {
        'total_books': len(df),
        'average_price': df['price'].mean(),
        'average_rating': df['rating'].mean()
    }