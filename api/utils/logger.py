import datetime
import os
import json


class Logger:
    def __init__(self):
        """Initialize logger with logs directory."""
        self.log_file = 'logs/api.log'
        self.file_logging_enabled = self._check_file_logging()
        
        if self.file_logging_enabled:
            try:
                if not os.path.exists('logs'):
                    os.makedirs('logs')
            except (OSError, PermissionError):
                self.file_logging_enabled = False

    def _check_file_logging(self):
        """Check if file logging is possible (not in read-only environment)."""
        try:
            # Try to create a test file in the logs directory
            test_dir = 'logs'
            test_file = os.path.join(test_dir, 'test.log')
            
            if not os.path.exists(test_dir):
                os.makedirs(test_dir)
            
            with open(test_file, 'w') as f:
                f.write('test')
            
            # Clean up test file
            os.remove(test_file)
            return True
        except (OSError, PermissionError):
            # File system is read-only or we don't have write permissions
            return False

    def __log(self, level, message):
        """Internal method to log messages."""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f'[{timestamp}] [{level}] {message}\n'
        
        # Print to console (always available)
        print(log_message.strip())
        
        # Write to file only if file logging is enabled
        if self.file_logging_enabled:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(log_message)
            except (OSError, PermissionError):
                # If file writing fails, disable file logging for future calls
                self.file_logging_enabled = False

    def debug(self, message):
        """Log a debug message."""
        self.__log('DEBUG', message)

    def info(self, message):
        """Log an info message."""
        self.__log('INFO', message)

    def warning(self, message):
        """Log a warning message."""
        self.__log('WARNING', message)

    def error(self, message):
        """Log an error message."""
        self.__log('ERROR', message)

    def critical(self, message):
        """Log a critical message."""
        self.__log('CRITICAL', message)

    def log_request(self, method, path, status_code, duration_ms):
        """Log an API request."""
        message = f"API_CALL: method={method}, path={path}, status={status_code}, duration={duration_ms}ms"
        self.info(message)

    def log_error(self, method, path, error_type, error_message):
        """Log an API error."""
        message = f"API_ERROR: method={method}, path={path}, type={error_type}, message={error_message}"
        self.error(message)

    def log_ml_prediction(self, book_id, prediction, confidence):
        """Log an ML prediction."""
        message = f"ML_PREDICTION: book_id={book_id}, prediction={prediction}, confidence={confidence}"
        self.info(message)

    def log_request_json(self, log_data):
        """Log an API request in JSON format."""
        message = f"API_CALL: {json.dumps(log_data)}"
        self.info(message)

    def log_error_json(self, error_data):
        """Log an API error in JSON format."""
        message = f"API_ERROR: {json.dumps(error_data)}"
        self.error(message)

    def log_ml_prediction_json(self, prediction_data):
        """Log an ML prediction in JSON format."""
        message = f"ML_PREDICTION: {json.dumps(prediction_data)}"
        self.info(message)


# Global logger instance
logger = Logger()