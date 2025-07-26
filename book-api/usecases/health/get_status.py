from api.core.database import get_books_dataframe

def get_health_status_usecase():
    """
    Verifica se o arquivo CSV está presente e pode ser carregado com sucesso.
    """
    try:
        df = get_books_dataframe()
        return {
            "status": "ok",
            "csv_available": True,
            "total_books": len(df)
        }
    except Exception as e:
        return {
            "status": "error",
            "csv_available": False,
            "error": str(e)
        }
