import logging
import sys
from logging.handlers import RotatingFileHandler
from app.utils.constant import LOG_DIR, LOG_FILE_PATH

# Make sure log dir exists
LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers (especially during dev reloads)
    if logger.hasHandlers():
        return logger

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console Handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Rotating File Handler (logs/app.log)
    file_handler = RotatingFileHandler(
        LOG_FILE_PATH, maxBytes=5 * 1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
