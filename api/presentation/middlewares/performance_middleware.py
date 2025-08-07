import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from api.utils.logger import logger


class PerformanceMiddleware(BaseHTTPMiddleware):
    """Middleware to capture performance metrics for all API calls."""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        try:
            # Process the request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            duration_ms = round(duration * 1000, 2)
            
            # Log the request/response
            logger.log_request(
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=duration_ms
            )
            
            # Add performance headers
            response.headers["X-Response-Time"] = f"{duration_ms}ms"
            response.headers["X-Request-ID"] = str(time.time())
            
            return response
            
        except Exception as e:
            # Calculate duration even for errors
            duration = time.time() - start_time
            duration_ms = round(duration * 1000, 2)
            
            # Log the error
            logger.log_error(
                method=request.method,
                path=request.url.path,
                error_type=type(e).__name__,
                error_message=str(e)
            )
            
            # Re-raise the exception
            raise 