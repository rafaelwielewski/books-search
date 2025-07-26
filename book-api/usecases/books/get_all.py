from api.core.database import get_books_list

def get_all_books_usecase() -> list[dict]:
    return get_books_list()