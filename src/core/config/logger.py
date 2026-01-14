import logging
import sys

from src.core.config.settings import app_settings


def setup_logger(name: str = "techpark") -> logging.Logger:
    """Настройка логгера"""
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if app_settings.debug else logging.INFO)
    
    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if app_settings.debug else logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


logger = setup_logger()

