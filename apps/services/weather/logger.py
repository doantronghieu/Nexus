"""
Logging configuration for the Weather Service.
"""
import logging
import sys
from typing import Optional
from .config import settings


def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        name: The name for the logger
        level: Optional logging level (defaults to DEBUG if settings.DEBUG is True)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    
    # Determine log level
    log_level = (level or "DEBUG") if settings.DEBUG else "INFO"
    logger.setLevel(log_level)
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger


# Create default logger instance
logger = setup_logger("weather_service")