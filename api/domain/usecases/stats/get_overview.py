from api.infra.database import get_books_dataframe

def get_stats_overview_usecase():
    df = get_books_dataframe()
    total_books = len(df)
    avg_price = round(df["price"].mean(), 2)
    rating_dist = df["rating"].value_counts().sort_index().to_dict()
    
    return {
        "total_books": total_books,
        "average_price": avg_price,
        "rating_distribution": rating_dist
    }