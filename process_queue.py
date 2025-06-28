#!/usr/bin/env python3

import yaml
from pathlib import Path
from logger import logger
import transcode_movie
import move_completed
import handle_failed
import sys

def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def scan_staging():
    config = load_config()
    if config.get('test_mode', False):
        staging = Path(config['paths']['test'])
        logger.info("Running in test mode - using test directory")
    else:
        staging = Path(config['paths']['staging'])
    plex = Path(config['paths']['plex'])
    if not staging.exists():
        logger.error(f"Staging directory not found: {staging}")
        return False
    plex_files = {f.name for f in plex.glob("*.mkv")} if plex.exists() else set()
    queue = []
    for file in staging.glob("*.mkv"):
        if file.name in plex_files:
            logger.info(f"Skipping {file.name} - already in plex")
            continue
        if "-transcoded" in file.name:
            logger.info(f"Skipping {file.name} - already transcoded")
            continue
        queue.append(str(file))
        logger.info(f"Added to queue: {file.name}")
    if queue:
        with open('queue.txt', 'w') as f:
            f.write('\n'.join(queue))
        logger.info(f"Queue created with {len(queue)} files")
        return True
    else:
        logger.info("No new files to transcode")
        return False

def process_queue():
    if not scan_staging():
        logger.error("No queue file found. Run scan_staging.py first.")
        return False
    queue_file = Path('queue.txt')
    if not queue_file.exists():
        logger.error("No queue file found. Run scan_staging.py first.")
        return False
    with open(queue_file, 'r') as f:
        files = f.read().splitlines()
    logger.info(f"Processing {len(files)} files from queue")
    for file in files:
        logger.info(f"Processing: {file}")
        if transcode_movie.transcode_file(file, load_config()):
            logger.info(f"Transcode successful: {file}")
            if move_completed.move_completed(file.replace('.mkv', '-transcoded.mkv')):
                logger.info(f"Move completed: {file}")
            else:
                logger.error(f"Move failed: {file}")
        else:
            logger.error(f"Transcode failed: {file}")
            if handle_failed.handle_failed(file):
                logger.info(f"Failed file handled: {file}")
            else:
                logger.error(f"Failed file handling failed: {file}")
    queue_file.unlink()
    logger.info("Queue processing complete")
    return True

if __name__ == "__main__":
    process_queue() 