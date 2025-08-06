from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

async def validation_error_handler(request: Request, exc: ValidationError):
    """
    Handler for Pydantic ValidationError exceptions
    """
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Erro de validação dos dados",
            "errors": [
                {
                    "loc": err["loc"],
                    "msg": err["msg"],
                    "type": err["type"]
                } for err in exc.errors()
            ]
        }
    )

async def request_validation_error_handler(request: Request, exc: RequestValidationError):
    """
    Handler for FastAPI RequestValidationError exceptions
    """
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Erro de validação da requisição",
            "errors": [
                {
                    "loc": err["loc"],
                    "msg": err["msg"],
                    "type": err["type"]
                } for err in exc.errors()
            ]
        }
    )
