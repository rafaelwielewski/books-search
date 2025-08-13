import datetime
import os
import json
import threading
from typing import Dict, List, Any, Optional
from collections import deque
import redis
class Logger:
    """Unified logger for serverless environments with Redis, file, and memory storage."""
    
    def __init__(self, max_logs: int = 1000):
        self.max_logs = max_logs
        self.logs = deque(maxlen=max_logs)
        self.lock = threading.Lock()
        
        # Check environment
        self.is_local = self._is_local_environment()
        
        # Initialize storage backends
        self.redis_client = None
        self.file_logging_enabled = False
        
        # Setup storage based on environment
        self._setup_storage()
    
    def _is_local_environment(self) -> bool:
        print(os.getenv('ENV'))
        """Check if we're running in local environment."""
        local_indicators = [
            os.getenv('ENV') == 'LOCAL',
        ]
        return any(local_indicators)
    
    def _is_serverless_environment(self) -> bool:
        """Check if we're running in a serverless environment."""
        serverless_indicators = [
            'VERCEL' in os.environ,
            'AWS_LAMBDA_FUNCTION_NAME' in os.environ,
            'FUNCTION_TARGET' in os.environ,
            'K_SERVICE' in os.environ,  # Google Cloud Run
        ]
        return any(serverless_indicators)
    
    def _setup_storage(self):
        """Setup storage backends based on environment."""
        if not self.is_local:
            # Try Redis for non-local environments
            self._setup_redis()
        
        # Setup file logging for local development
        if self.is_local:
            self._setup_file_logging()
    
    def _setup_redis(self):
        """Setup Redis connection."""
        try:
            redis_url = os.getenv('REDIS_URL')
            if redis_url and redis:
                self.redis_client = redis.from_url(redis_url)
                # Test connection
                self.redis_client.ping()
                self.redis_available = True
                print("✅ Redis connection established for logging")
            else:
                print("⚠️  REDIS_URL not found or redis not available, Redis logging disabled")
        except Exception as e:
            print(f"❌ Redis connection failed: {e}")
            self.redis_available = False
    
    def _setup_file_logging(self):
        """Setup file logging for local development."""
        try:
            log_dir = 'logs'
            log_file = os.path.join(log_dir, 'api.log')
            
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            # Test write
            with open(log_file, 'a') as f:
                f.write('')
            
            self.log_file = log_file
            self.file_logging_enabled = True
            print("✅ File logging enabled for local development")
        except Exception as e:
            print(f"❌ File logging setup failed: {e}")
            self.file_logging_enabled = False
    
    def _store_in_redis(self, log_data: Dict[str, Any]) -> bool:
        """Store log entry in Redis."""
        if not self.redis_available or not self.redis_client:
            return False
        
        try:
            # Add timestamp if not present
            if 'timestamp' not in log_data:
                log_data['timestamp'] = datetime.datetime.now().isoformat()
            
            # Store in Redis with expiration (7 days)
            log_key = f"log:{datetime.datetime.now().timestamp()}"
            self.redis_client.setex(
                log_key,
                7 * 24 * 60 * 60,  # 7 days in seconds
                json.dumps(log_data)
            )
            
            # Add to sorted set for easy retrieval
            self.redis_client.zadd(
                'logs:timeline',
                {log_key: datetime.datetime.now().timestamp()}
            )
            
            return True
        except Exception as e:
            print(f"Failed to store log in Redis: {e}")
            return False
    
    def _store_in_file(self, log_data: Dict[str, Any]) -> bool:
        """Store log entry in file."""
        if not self.file_logging_enabled:
            return False
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_data) + '\n')
            return True
        except Exception as e:
            print(f"Failed to store log in file: {e}")
            return False
    
    def __log(self, level: str, message: str, data: Optional[Dict] = None):
        """Internal method to log messages."""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = {
            'timestamp': timestamp,
            'level': level,
            'message': message,
            'data': data
        }
        
        # Print to console (always available)
        print(f'[{timestamp}] [{level}] {message}')
        if data:
            print(f'Data: {json.dumps(data, indent=2)}')
        
        # Store in memory for all environments
        with self.lock:
            self.logs.append(log_entry)
        
        # Store in Redis for non-local environments
        if not self.is_local:
            self._store_in_redis(log_entry)
        
        # Store in file for local development
        if self.is_local:
            self._store_in_file(log_entry)
    
    def debug(self, message: str, data: Optional[Dict] = None):
        """Log a debug message."""
        self.__log('DEBUG', message, data)
    
    def info(self, message: str, data: Optional[Dict] = None):
        """Log an info message."""
        self.__log('INFO', message, data)
    
    def warning(self, message: str, data: Optional[Dict] = None):
        """Log a warning message."""
        self.__log('WARNING', message, data)
    
    def error(self, message: str, data: Optional[Dict] = None):
        """Log an error message."""
        self.__log('ERROR', message, data)
    
    def critical(self, message: str, data: Optional[Dict] = None):
        """Log a critical message."""
        self.__log('CRITICAL', message, data)
    
    def log_request(self, method: str, path: str, status_code: int, duration_ms: float):
        """Log an API request."""
        data = {
            'method': method,
            'path': path,
            'status_code': status_code,
            'duration_ms': duration_ms
        }
        self.info(f"API_CALL: method={method}, path={path}, status={status_code}, duration={duration_ms}ms", data)
    
    def log_error(self, method: str, path: str, error_type: str, error_message: str):
        """Log an API error."""
        data = {
            'method': method,
            'path': path,
            'error_type': error_type,
            'error_message': error_message
        }
        self.error(f"API_ERROR: method={method}, path={path}, type={error_type}, message={error_message}", data)
    
    def log_ml_prediction(self, book_id: str, prediction: float, confidence: float):
        """Log an ML prediction."""
        data = {
            'book_id': book_id,
            'prediction': prediction,
            'confidence': confidence
        }
        self.info(f"ML_PREDICTION: book_id={book_id}, prediction={prediction}, confidence={confidence}", data)
    
    def log_request_json(self, log_data: Dict[str, Any]):
        """Log an API request in JSON format."""
        self.info(f"API_CALL: {json.dumps(log_data)}", log_data)
    
    def log_error_json(self, error_data: Dict[str, Any]):
        """Log an API error in JSON format."""
        self.error(f"API_ERROR: {json.dumps(error_data)}", error_data)
    
    def log_ml_prediction_json(self, prediction_data: Dict[str, Any]):
        """Log an ML prediction in JSON format."""
        self.info(f"ML_PREDICTION: {json.dumps(prediction_data)}", prediction_data)
    
    def get_logs(self, level: Optional[str] = None, limit: Optional[int] = None) -> List[Dict]:
        """Get stored logs, optionally filtered by level."""
        logs = []
        
        # Get from memory
        with self.lock:
            memory_logs = list(self.logs)
        
        # Get from file if available
        if self.file_logging_enabled:
            try:
                file_logs = self._get_file_logs()
                logs.extend(file_logs)
            except Exception as e:
                print(f"Failed to get logs from file: {e}")
        
        # Add memory logs
        logs.extend(memory_logs)
        
        # Remove duplicates and sort by timestamp
        unique_logs = []
        seen_timestamps = set()
        for log in logs:
            timestamp = log.get('timestamp', '')
            if timestamp not in seen_timestamps:
                unique_logs.append(log)
                seen_timestamps.add(timestamp)
        
        # Sort by timestamp (newest first)
        unique_logs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        # Filter by level
        if level:
            unique_logs = [log for log in unique_logs if log.get('level') == level]
        
        # Apply limit
        if limit:
            unique_logs = unique_logs[:limit]
        
        return unique_logs
    
    def _get_file_logs(self) -> List[Dict]:
        """Get logs from file."""
        if not self.file_logging_enabled:
            return []
        
        try:
            logs = []
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        log_entry = json.loads(line.strip())
                        logs.append(log_entry)
                    except json.JSONDecodeError:
                        continue
            
            return logs
        except Exception as e:
            print(f"Failed to retrieve logs from file: {e}")
            return []
    
    def get_api_calls(self, limit: Optional[int] = None) -> List[Dict]:
        """Get API call logs."""
        logs = self.get_logs(limit=limit)
        api_calls = []
        
        for log in logs:
            if log.get('data') and 'method' in log['data'] and 'path' in log['data']:
                api_calls.append(log['data'])
        
        return api_calls
    
    def get_errors(self, limit: Optional[int] = None) -> List[Dict]:
        """Get error logs."""
        logs = self.get_logs(level='ERROR', limit=limit)
        errors = []
        
        for log in logs:
            if log.get('data') and 'error_type' in log['data']:
                errors.append(log['data'])
        
        return errors
    
    def get_ml_predictions(self, limit: Optional[int] = None) -> List[Dict]:
        """Get ML prediction logs."""
        logs = self.get_logs(limit=limit)
        predictions = []
        
        for log in logs:
            if log.get('data') and 'book_id' in log['data'] and 'prediction' in log['data']:
                predictions.append(log['data'])
        
        return predictions
    
    def clear_logs(self) -> bool:
        """Clear all stored logs."""
        try:
            # Clear memory logs
            with self.lock:
                self.logs.clear()
            
            # Clear file logs
            if self.file_logging_enabled:
                try:
                    with open(self.log_file, 'w') as f:
                        f.write('')
                except Exception as e:
                    print(f"Failed to clear file logs: {e}")
            
            return True
        except Exception as e:
            print(f"Failed to clear logs: {e}")
            return False


# Global logger instance
logger = Logger() 