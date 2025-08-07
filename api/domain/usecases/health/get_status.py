from api.infra.repository.book_repository import get_books_dataframe


def get_health_status_usecase():
    """Check application health status."""
    try:
        df = get_books_dataframe()
        return {
            "status": "healthy",
            "message": "API funcionando corretamente",
            "data": {
                "csv_loaded": True,
                "total_books": len(df)
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
