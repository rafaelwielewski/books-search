from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

class MLFeatures(BaseModel):
    """Features extracted from a book for ML processing"""
    book_id: str
    title_length: int
    category_encoded: int
    price_normalized: float
    rating_normalized: float
    has_discount: bool
    price_category: str
    rating_category: str

class TrainingData(BaseModel):
    """Training data for ML models"""
    features: List[MLFeatures]
    targets: Dict[str, List[float]]
    metadata: Dict[str, Any]

class MLPrediction(BaseModel):
    """ML model prediction for a book"""
    book_id: str
    model_name: str
    prediction: float
    confidence: float
    features_used: List[str]
    timestamp: datetime

class ModelInfo(BaseModel):
    """Information about an ML model"""
    model_name: str
    description: str
    version: str
    features_required: List[str]
    target_variable: str
    performance_metrics: Dict[str, float]
    last_updated: datetime
    is_active: bool 