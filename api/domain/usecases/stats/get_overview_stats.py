from api.infra.repository.book_repository import BookRepository


class GetStatsOverviewUseCase:
    """Use case for getting overview statistics of all books."""
    
    def __init__(self, book_repository: BookRepository):
        self.repository = book_repository
    
    def execute(self):
        """Execute the use case to get overview statistics of all books."""
        books = self.repository.get_books_list()
        
        if not books:
            return {
                'total_books': 0,
                'average_price': 0.0,
                'average_rating': 0.0
            }
        
        total_books = len(books)
        average_price = sum(book.price for book in books) / total_books
        average_rating = sum(book.rating for book in books) / total_books
        
        return {
            'total_books': total_books,
            'average_price': round(average_price, 2),
            'average_rating': round(average_rating, 2)
        }