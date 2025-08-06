from api.infra.database import get_books_list

def search_by_title_or_category_usecase(title: str = "", category: str = ""):
    books = get_books_list()
    title = title.lower()
    category = category.lower()
    results = [
        b for b in books
        if (title in b["title"].lower() if title else True)
        and (category in b["category"].lower() if category else True)
    ]
    return results