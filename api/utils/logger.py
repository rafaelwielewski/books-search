import datetime
import os


class Logger:
    def __log(self, level, message):
        if not os.path.exists('logs'):
            os.makedirs('logs')
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f'[{timestamp}] [{level}] {message}\n'
        print(log_message.strip())

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


# Instância global do logger
logger = Logger()