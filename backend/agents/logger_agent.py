# backend/agents/logger_agent.py
from .base_agent import BaseAgent
from .log_level import LogLevel
import logging
from threading import Lock

class LoggerAgent(BaseAgent):
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(LoggerAgent, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        name: str = "AgentLogger",
        log_file: str = "agent.log",
        level: LogLevel = LogLevel.DEBUG,
        log_to_console: bool = False
    ):
        if hasattr(self, "logger"):  # Avoid re-initializing
            return

        self.logger = logging.getLogger(name)
        self.logger.setLevel(self._map_log_level(level))

        if not self.logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

            if log_to_console:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                self.logger.addHandler(console_handler)

    def run(self, message: str, level: LogLevel = LogLevel.INFO):
        log_method = getattr(self.logger, level.value.lower(), self.logger.info)
        log_method(message)

    def _map_log_level(self, level: LogLevel):
        return {
            LogLevel.DEBUG: logging.DEBUG,
            LogLevel.INFO: logging.INFO,
            LogLevel.WARNING: logging.WARNING,
            LogLevel.ERROR: logging.ERROR,
            LogLevel.CRITICAL: logging.CRITICAL
        }.get(level, logging.INFO)
