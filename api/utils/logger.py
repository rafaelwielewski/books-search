from typing import Any
import os

class Logger:
    def __log(self, msg: Any, level_type: str):
        if not self.__is_local():
            return
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
        return os.getenv('ENVIRONMENT') == 'LOCAL'


logger = Logger()