#!/usr/bin/env python3

import yaml
from pathlib import Path
from logger import logger
import shutil
import sys

def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def handle_failed(source_file):
    config = load_config()
    
    # Use test directory if in test mode
    if config.get('test_mode', False):
        staging = Path(config['paths']['test'])
        logger.info("Running in test mode - using test directory")
    else:
        staging = Path(config['paths']['staging'])
    
    # Create failed directory in staging
    failed_dir = staging / "failed"
    failed_dir.mkdir(exist_ok=True)
    
    # Get paths
    source = Path(source_file)
    if not source.exists():
        logger.error(f"Source file not found: {source}")
        return False
    
    # Get transcoded file path if it exists
    transcoded = source.parent / f"{source.stem}-transcoded{source.suffix}"
    
    try:
        # Move original to failed directory
        logger.info(f"Moving {source.name} to failed directory")
        shutil.move(str(source), str(failed_dir / source.name))
        
        # Move transcoded file if it exists
        if transcoded.exists():
            logger.info(f"Moving partial transcode {transcoded.name} to failed directory")
            shutil.move(str(transcoded), str(failed_dir / transcoded.name))
        
        logger.info("Failed files moved successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error moving failed files: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logger.error("Usage: handle_failed.py <source_file>")
        sys.exit(1)
    
    if handle_failed(sys.argv[1]):
        sys.exit(0)
    else:
        sys.exit(1) 