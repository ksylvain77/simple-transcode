#!/usr/bin/env python3

import logging
from logging.handlers import RotatingFileHandler
import yaml
from pathlib import Path

def setup_logger():
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Create logs directory if it doesn't exist
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # Set up logger
    logger = logging.getLogger('transcode')
    logger.setLevel(logging.INFO)
    
    # Format: timestamp - level - message
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # File handler with rotation (10MB per file, keep 5 backups)
    file_handler = RotatingFileHandler(
        log_dir / 'transcode.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

# Create logger instance
logger = setup_logger()

# Quick test if run directly
if __name__ == "__main__":
    logger.info("Logger initialized")
    logger.warning("This is a test warning")
    logger.error("This is a test error") 