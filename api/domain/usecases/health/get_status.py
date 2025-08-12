from api.domain.repositories.book_repository import BookRepository


class GetHealthStatusUseCase:
    """Use case for checking application health status."""
    
    def __init__(self, book_repository: BookRepository):
        self.repository = book_repository
    
    def execute(self):
        """Execute the use case to check application health status."""
        try:
            books = self.repository.get_books_list()
            return {
                "status": "healthy",
                "message": "API funcionando corretamente",
                "data": {
                    "csv_loaded": True,
                    "total_books": len(books)
                }
            }
        except FileNotFoundError:
            return {
                "status": "unhealthy",
                "message": "Arquivo de dados não encontrado",
                "data": {
                    "csv_loaded": False,
                    "total_books": 0
                }
            }
        except Exception as e:
            return {
                "status": "unhealthy", 
                "message": f"Erro ao verificar dados: {str(e)}",
                "data": {
                    "csv_loaded": False,
                    "total_books": 0
                }
            }
