#!/usr/bin/env python3

import yaml
from pathlib import Path
from logger import logger
import shutil
import sys

def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def move_completed(transcoded_file):
    config = load_config()
    plex = Path(config['paths']['plex'])
    
    # Make sure plex directory exists
    plex.mkdir(parents=True, exist_ok=True)
    
    # Get paths
    transcoded = Path(transcoded_file)
    if not transcoded.exists():
        logger.error(f"Transcoded file not found: {transcoded}")
        return False
    
    # Get original file path (remove -transcoded from name)
    original = transcoded.parent / transcoded.name.replace("-transcoded", "")
    if not original.exists():
        logger.error(f"Original file not found: {original}")
        return False
    
    # Get plex destination
    plex_dest = plex / transcoded.name.replace("-transcoded", "")
    
    try:
        # Move transcoded file to plex
        logger.info(f"Moving {transcoded.name} to plex")
        shutil.move(str(transcoded), str(plex_dest))
        
        # Delete original file
        logger.info(f"Deleting original file: {original.name}")
        original.unlink()
        
        logger.info("Move completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error moving files: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logger.error("Usage: move_completed.py <transcoded_file>")
        sys.exit(1)
    
    if move_completed(sys.argv[1]):
        sys.exit(0)
    else:
        sys.exit(1) 