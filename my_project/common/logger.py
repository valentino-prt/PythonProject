import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from common.paths import LOG_DIR

try:
    import colorlog
except ImportError:
    colorlog = None


def _get_file_handler(log_file: Path) -> logging.Handler:
    handler = RotatingFileHandler(
        log_file, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    handler.setFormatter(
        logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")
    )
    return handler


def _get_stream_handler() -> logging.Handler:
    if colorlog:
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt="%H:%M:%S",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
    else:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S"
        )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    return handler


def configure_logger(name: str = __name__) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        logger.addHandler(_get_stream_handler())
        logger.addHandler(_get_file_handler(LOG_DIR / "app.log"))
    return logger
