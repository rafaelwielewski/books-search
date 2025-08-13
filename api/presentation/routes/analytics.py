from typing import Dict, List, Any
from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import json
import os
from collections import defaultdict, Counter
from api.presentation.routes.router import DefaultRouter
from api.utils.logger import logger

router = APIRouter(route_class=DefaultRouter)

@router.get("/metrics", summary="Get API metrics and usage statistics")
async def get_api_metrics():
    """
    Get API performance metrics and usage statistics.
    """
    try:
        # Get logs from memory instead of reading files
        api_calls = logger.get_api_calls()
        errors = logger.get_errors()
        
        metrics = {
            "total_requests": 0,
            "requests_by_endpoint": {},
            "requests_by_method": {},
            "average_response_time": 0.0,
            "error_rate": 0.0,
            "top_endpoints": [],
            "recent_activity": []
        }
        
        # Calculate metrics
        if api_calls:
            metrics["total_requests"] = len(api_calls)
            
            # Endpoint breakdown
            endpoint_counts = Counter(call["path"] for call in api_calls)
            metrics["requests_by_endpoint"] = dict(endpoint_counts)
            
            # Method breakdown
            method_counts = Counter(call["method"] for call in api_calls)
            metrics["requests_by_method"] = dict(method_counts)
            
            # Average response time
            response_times = [call["duration_ms"] for call in api_calls if "duration_ms" in call]
            if response_times:
                metrics["average_response_time"] = sum(response_times) / len(response_times)
            
            # Error rate
            total_requests = len(api_calls) + len(errors)
            if total_requests > 0:
                metrics["error_rate"] = len(errors) / total_requests * 100
            
            # Top endpoints
            metrics["top_endpoints"] = [
                {"endpoint": endpoint, "count": count}
                for endpoint, count in endpoint_counts.most_common(5)
            ]
            
            # Recent activity (last 10 requests)
            recent_calls = sorted(api_calls, key=lambda x: x.get("timestamp", ""), reverse=True)[:10]
            metrics["recent_activity"] = [
                {
                    "timestamp": call.get("timestamp", ""),
                    "method": call["method"],
                    "path": call["path"],
                    "status_code": call["status_code"],
                    "duration_ms": call["duration_ms"]
                }
                for call in recent_calls
            ]
        
        return metrics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating metrics: {str(e)}")


@router.get("/ml-predictions", summary="Get ML prediction statistics")
async def get_ml_predictions():
    """
    Get ML prediction statistics and recent predictions.
    """
    try:
        # Get ML predictions from memory
        ml_predictions = logger.get_ml_predictions()
        
        predictions = {
            "total_predictions": 0,
            "average_confidence": 0.0,
            "predictions_by_book": {},
            "recent_predictions": []
        }
        
        if ml_predictions:
            predictions["total_predictions"] = len(ml_predictions)
            
            # Average confidence
            confidences = [pred["confidence"] for pred in ml_predictions if "confidence" in pred]
            if confidences:
                predictions["average_confidence"] = sum(confidences) / len(confidences)
            
            # Predictions by book
            book_predictions = defaultdict(list)
            for pred in ml_predictions:
                if "book_id" in pred:
                    book_predictions[pred["book_id"]].append(pred)
            
            predictions["predictions_by_book"] = {
                book_id: {
                    "count": len(preds),
                    "average_prediction": sum(p["prediction"] for p in preds) / len(preds),
                    "average_confidence": sum(p["confidence"] for p in preds) / len(preds)
                }
                for book_id, preds in book_predictions.items()
            }
            
            # Recent predictions
            recent_preds = sorted(ml_predictions, key=lambda x: x.get("timestamp", ""), reverse=True)[:10]
            predictions["recent_predictions"] = [
                {
                    "timestamp": pred.get("timestamp", ""),
                    "book_id": pred["book_id"],
                    "prediction": pred["prediction"],
                    "confidence": pred["confidence"]
                }
                for pred in recent_preds
            ]
        
        return predictions
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating ML predictions: {str(e)}")


@router.get("/performance", summary="Get detailed performance metrics")
async def get_performance_metrics():
    """
    Get detailed performance metrics.
    """
    try:
        # Get logs from memory
        api_calls = logger.get_api_calls()
        errors = logger.get_errors()
        
        performance = {
            "response_time_distribution": {},
            "endpoint_performance": {},
            "error_breakdown": {},
            "system_health": {}
        }
        
        if api_calls:
            # Response time distribution
            response_times = [call["duration_ms"] for call in api_calls if "duration_ms" in call]
            if response_times:
                sorted_times = sorted(response_times)
                performance["response_time_distribution"] = {
                    "min": min(response_times),
                    "max": max(response_times),
                    "median": sorted_times[len(sorted_times)//2],
                    "p95": sorted_times[int(len(sorted_times)*0.95)] if len(sorted_times) > 20 else max(response_times),
                    "p99": sorted_times[int(len(sorted_times)*0.99)] if len(sorted_times) > 100 else max(response_times)
                }
            
            # Endpoint performance
            endpoint_perf = defaultdict(list)
            for call in api_calls:
                if "path" in call and "duration_ms" in call:
                    endpoint_perf[call["path"]].append(call["duration_ms"])
            
            performance["endpoint_performance"] = {
                endpoint: {
                    "avg_response_time": sum(times) / len(times),
                    "request_count": len(times),
                    "min_response_time": min(times),
                    "max_response_time": max(times)
                }
                for endpoint, times in endpoint_perf.items()
            }
            
            # Error breakdown
            error_types = Counter(error.get("error_type", "Unknown") for error in errors)
            performance["error_breakdown"] = dict(error_types)
            
            # System health
            total_requests = len(api_calls) + len(errors)
            performance["system_health"] = {
                "uptime_percentage": 100 - (len(errors) / total_requests * 100) if total_requests > 0 else 100,
                "total_requests": total_requests,
                "error_count": len(errors),
                "success_rate": len(api_calls) / total_requests * 100 if total_requests > 0 else 100
            }
        
        return performance
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating performance metrics: {str(e)}")


@router.get("/logs", summary="Get raw logs")
async def get_logs(level: str | None = None, limit: int = 100):
    """
    Get raw logs from memory.
    """
    try:
        logs = logger.get_logs(level=level, limit=limit)
        return {
            "logs": logs,
            "total_count": len(logs),
            "level_filter": level,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving logs: {str(e)}")


@router.delete("/logs", summary="Clear all logs")
async def clear_logs():
    """
    Clear all stored logs.
    """
    try:
        logger.clear_logs()
        return {"message": "All logs cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing logs: {str(e)}") 