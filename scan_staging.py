#!/usr/bin/env python3

import yaml
from pathlib import Path
from logger import logger

def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def scan_staging():
    config = load_config()
    
    # Use test directory if in test mode
    if config.get('test_mode', False):
        staging = Path(config['paths']['test'])
        logger.info("Running in test mode - using test directory")
    else:
        staging = Path(config['paths']['staging'])
    
    plex = Path(config['paths']['plex'])
    
    if not staging.exists():
        logger.error(f"Staging directory not found: {staging}")
        return False
    
    # Get list of existing files in plex
    plex_files = {f.name for f in plex.glob("*.mkv")} if plex.exists() else set()
    
    # Find new MKV files in staging
    queue = []
    for file in staging.glob("*.mkv"):
        # Skip if already in plex
        if file.name in plex_files:
            logger.info(f"Skipping {file.name} - already in plex")
            continue
        
        # Skip if already transcoded
        if "-transcoded" in file.name:
            logger.info(f"Skipping {file.name} - already transcoded")
            continue
        
        queue.append(str(file))
        logger.info(f"Added to queue: {file.name}")
    
    # Write queue to file
    if queue:
        with open('queue.txt', 'w') as f:
            f.write('\n'.join(queue))
        logger.info(f"Queue created with {len(queue)} files")
        return True
    else:
        logger.info("No new files to transcode")
        return False

if __name__ == "__main__":
    scan_staging() 