from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
from datetime import datetime

from api.infra.repository.book_repository import BookRepository
from api.domain.usecases.books.get_all_books import GetAllBooksUseCase
from api.utils.logger import logger
from api.presentation.routes.router import DefaultRouter

router = APIRouter(route_class=DefaultRouter)
