
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.presentation.routes import books, categories, stats, health, auth, scraping
from api.presentation.middlewares.error_handlers import validation_error_handler, request_validation_error_handler
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Book API",
    version="1.0.0",
    description="API para consulta de livros, categorias e estatísticas."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router, prefix="/api/v1/books", tags=["Books"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(stats.router, prefix="/api/v1/stats", tags=["Stats"])
app.include_router(health.router, prefix="/api/v1/health", tags=["Health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(scraping.router, prefix="/api/v1/scraping", tags=["Scraping"])   

app.add_exception_handler(ValidationError, validation_error_handler)
app.add_exception_handler(RequestValidationError, request_validation_error_handler)

@app.get("/")
def root():
    return {"message": "Book API - consulte /docs para documentação."}

