from api.infra.database import get_books_list

def get_top_rated_books_usecase(limit: int = 0):
    books = get_books_list()
    sorted_books = sorted(books, key=lambda x: x["rating"], reverse=True)
    if limit != 0:
        sorted_books = sorted_books[:limit]
    return sorted_books