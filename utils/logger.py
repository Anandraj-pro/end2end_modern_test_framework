import os
import logging
from logging.handlers import RotatingFileHandler
import threading
from colorama import init, Fore, Style

# Initialize colorama for colored terminal logs
init(autoreset=True)

class LogColorsFormatter(logging.Formatter):
    """Custom logging formatter that injects color escape sequences in CLI output."""
    
    LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)s)"
    
    LEVEL_COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT
    }
    
    def format(self, record):
        color = self.LEVEL_COLORS.get(record.levelno, "")
        original_msg = super().format(record)
        if color:
            return f"{color}{original_msg}{Style.RESET_ALL}"
        return original_msg

class FrameworkLogger:
    """Thread-safe Singleton Logger ensuring a single logger instance is used across concurrent executions."""
    _logger = None
    _lock = threading.Lock()
    
    @classmethod
    def get_logger(cls, name="E2E_Automation"):
        with cls._lock:
            if cls._logger is None:
                # Resolve logs directory path safely
                log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
                os.makedirs(log_dir, exist_ok=True)
                
                cls._logger = logging.getLogger(name)
                cls._logger.setLevel(logging.DEBUG)
                
                # Prevent log records from climbing up standard pytest propagation
                cls._logger.propagate = False
                
                # 1. Console Stream Handler
                console_handler = logging.StreamHandler()
                console_handler.setLevel(logging.INFO)
                console_formatter = LogColorsFormatter(LogColorsFormatter.LOG_FORMAT)
                console_handler.setFormatter(console_formatter)
                
                # 2. File Handler with Rotation (max 5MB, keep 5 historic logs)
                log_file_path = os.path.join(log_dir, "framework.log")
                file_handler = RotatingFileHandler(
                    log_file_path,
                    maxBytes=5 * 1024 * 1024,
                    backupCount=5,
                    encoding="utf-8"
                )
                file_handler.setLevel(logging.DEBUG)
                file_formatter = logging.Formatter(
                    "%(asctime)s [%(levelname)s] [%(threadName)s] %(message)s (%(filename)s:%(lineno)s)"
                )
                file_handler.setFormatter(file_formatter)
                
                # Bind handlers
                cls._logger.addHandler(console_handler)
                cls._logger.addHandler(file_handler)
                
        return cls._logger

# Export global logger instance directly
logger = FrameworkLogger.get_logger()
