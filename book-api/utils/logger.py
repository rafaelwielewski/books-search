from typing import Any
import logging
import os

class Logger:
    def __log(self, msg: Any, level_type: str):
        if not self.__is_local():
            logger = logging.getLogger(__name__)
            log_method = getattr(logger, level_type, logger.info)
            log_method(msg)
        else:
            print(f"{level_type.upper()}: {msg}")

    def debug(self, msg: Any):
        self.__log(msg, 'debug')

    def info(self, msg: Any):
        self.__log(msg, 'info')

    def warning(self, msg: Any):
        self.__log(msg, 'warning')

    def error(self, msg: Any):
        self.__log(msg, 'error')

    def critical(self, msg: Any):
        self.__log(msg, 'critical')

    def __is_local(self) -> bool:
        return self.settings.environment in [os.getenv("ENVIRONMENT", "LOCAL")]


logger = Logger()