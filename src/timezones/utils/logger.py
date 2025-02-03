import logging
from logging.handlers import RotatingFileHandler
import os

LOGFILE_PATH = "app.log"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
NUM_BACKUPS = 3


def get_log_level():
    return os.getenv("LOG_LEVEL", "INFO").upper()


def setup_logger(name, log_file, level=logging.INFO):
    """Function to setup a logger"""
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(filename)s] %(message)s"
    )

    # Remove existing handlers
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        logger.handlers.clear()

    # File handler with log rotation
    file_handler = RotatingFileHandler(
        log_file, maxBytes=MAX_LOG_SIZE, backupCount=NUM_BACKUPS
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Initialize the logger
app_logger = setup_logger(
    "app_logger", LOGFILE_PATH, level=getattr(logging, get_log_level())
)
