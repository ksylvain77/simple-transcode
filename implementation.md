# Simple Transcode Implementation

## 1. logger.py
- Basic logging setup with rotation
- Simple format: timestamp + message
- Log to file in logs directory
- Quick test: write some test messages

## 2. transcode_movie.py
- Take file path as argument
- Use HandBrake CLI with GPU
- Keep it simple: one preset for all files
- Quick test: transcode one file

## 3. scan_staging.py
- List all MKV files in staging
- Skip if already in media folder
- Write paths to queue.txt
- Quick test: scan folder, check queue

## 4. move_completed.py
- Move file to media folder
- Delete original
- Quick test: move one file

## 5. handle_failed.py
- Move failed files to failed folder
- Quick test: simulate a failure

## 6. process_queue.py
- Read queue.txt
- Run transcode
- Move or handle failure
- Quick test: process one file

## Dependencies
- Python 3.12.3
- HandBrake CLI
- NVIDIA GPU drivers

## Config
- Just paths in config.yaml
- One simple encoding preset 