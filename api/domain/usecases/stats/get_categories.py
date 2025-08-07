from api.infra.repository.book_repository import get_books_list

def get_categories_stats_usecase():
    """Get statistics by category."""
    books = get_books_list()
    
    category_counts = {}
    for book in books:
        category = book.category
        category_counts[category] = category_counts.get(category, 0) + 1
    
    stats = []
    for category, count in category_counts.items():
        stats.append({
            'category': category,
            'count': count
        })
    
    return stats