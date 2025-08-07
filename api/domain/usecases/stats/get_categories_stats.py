from api.infra.repository.book_repository import BookRepository


class GetCategoriesStatsUseCase:
    """Use case for getting statistics by category."""
    
    def __init__(self, book_repository: BookRepository):
        self.repository = book_repository
    
    def execute(self):
        """Execute the use case to get statistics by category."""
        books = self.repository.get_books_list()
        
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