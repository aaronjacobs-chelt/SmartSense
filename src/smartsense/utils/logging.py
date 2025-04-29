
"""
Logging configuration for SmartSense.

This module provides a centralized logging configuration for the SmartSense
platform. It includes support for colored console output, file logging, and
structured log formatting.
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Union

import colorlog

# Default log levels for different components
DEFAULT_LOG_LEVELS = {
    "smartsense": logging.INFO,
    "smartsense.core": logging.INFO,
    "smartsense.sensors": logging.INFO,
    "smartsense.api": logging.INFO,
    "smartsense.utils": logging.INFO,
    "uvicorn": logging.WARNING,
    "fastapi": logging.WARNING,
    "pydantic": logging.WARNING,
}

# Log format for console output (colored)
CONSOLE_LOG_FORMAT = "%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(message)s"

# Log format for file output (more detailed)
FILE_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s"

# Color scheme for different log levels
LOG_COLORS = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}


def configure_logging(
    log_level: Union[int, str] = logging.INFO,
    console: bool = True,
    log_file: Optional[str] = None,
    component_levels: Optional[Dict[str, Union[int, str]]] = None,
) -> None:
    """
    Configure the logging system for SmartSense.
    
    Args:
        log_level: Base log level for all components
        console: Whether to log to console
        log_file: Path to log file (if None, file logging is disabled)
        component_levels: Dictionary of component-specific log levels
    """
    # Convert string log level to integer if needed
    if isinstance(log_level, str):
        log_level = getattr(logging, log_level.upper())
    
    # Set up the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Set up console logging if requested
    if console:
        console_handler = colorlog.StreamHandler(stream=sys.stdout)
        console_handler.setLevel(log_level)
        console_formatter = colorlog.ColoredFormatter(
            CONSOLE_LOG_FORMAT,
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors=LOG_COLORS,
        )
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
    
    # Set up file logging if requested
    if log_file:
        # Ensure the log directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir:
            Path(log_dir).mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter(
            FILE_LOG_FORMAT,
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    # Apply default component log levels
    for logger_name, level in DEFAULT_LOG_LEVELS.items():
        logging.getLogger(logger_name).setLevel(level)
    
    # Apply component-specific log levels if provided
    if component_levels:
        for logger_name, level in component_levels.items():
            # Convert string log level to integer if needed
            if isinstance(level, str):
                level = getattr(logging, level.upper())
            logging.getLogger(logger_name).setLevel(level)
    
    logging.info(f"Logging configured at level {logging.getLevelName(log_level)}")
    if log_file:
        logging.info(f"Log file: {log_file}")


def configure_file_rotation(
    log_file: str, 
    max_bytes: int = 10485760,  # 10 MB
    backup_count: int = 5,
) -> None:
    """
    Configure log rotation for an existing file handler.
    
    Args:
        log_file: Path to log file
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup files to keep
    """
    # Find and replace the existing FileHandler with a RotatingFileHandler
    root_logger = logging.getLogger()
    
    for handler in root_logger.handlers[:]:
        if isinstance(handler, logging.FileHandler) and handler.baseFilename == os.path.abspath(log_file):
            formatter = handler.formatter
            level = handler.level
            root_logger.removeHandler(handler)
            
            from logging.handlers import RotatingFileHandler
            rotating_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
            )
            rotating_handler.setLevel(level)
            rotating_handler.setFormatter(formatter)
            root_logger.addHandler(rotating_handler)
            
            logging.info(f"Configured log rotation for {log_file} (max size: {max_bytes/1024/1024:.1f} MB, backups: {backup_count})")
            return
    
    logging.warning(f"No file handler found for {log_file}, log rotation not configured")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific component.
    
    This is the preferred way to get a logger in the SmartSense application.
    It ensures that the logger has the correct name prefix and inherits
    the configured log level.
    
    Args:
        name: Name of the logger, typically __name__
    
    Returns:
        logging.Logger: Configured logger
    """
    # If the name doesn't start with 'smartsense', prefix it
    if not name.startswith('smartsense') and not name.startswith('__main__'):
        name = f"smartsense.{name}"
    
    return logging.getLogger(name)


# Initialize logging with default settings if not already configured
# This enables logging to work out of the box
if not logging.getLogger().handlers:
    configure_logging()
