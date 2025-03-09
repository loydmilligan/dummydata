"""
Logging utilities for the DummyData package.
"""

import os
import logging
import datetime
from pathlib import Path
from dummydata.config import LOG_DIR

def setup_logging(logger_name="DummyData", log_dir=LOG_DIR):
    """
    Configure and set up logging for the application.
    
    Args:
        logger_name (str): Name for the logger instance
        log_dir (Path): Directory where log files will be stored
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure logging
    timestamp = datetime.datetime.now().strftime('%Y%m%d')
    log_file = os.path.join(log_dir, f"orders_generation_{timestamp}.log")
    
    # Configure logger
    logger = logging.getLogger(logger_name)
    
    # Only set up handlers if they don't exist already
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create formatters and handlers
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger