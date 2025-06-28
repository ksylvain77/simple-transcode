# Transcoding Pipeline Scripts

## Scripts

### 1. scan_staging.py
- Scan staging folder for MKV files
- Check if already transcoded (exists in media/movies)
- Create list of files that need transcoding
- Output: queue.txt with file paths

### 2. transcode_movie.py
- Takes single MKV file path as argument
- Analyzes file with mediainfo to determine settings
- Reads encoding presets from config.yaml (blu-ray 4K, blu-ray 1080p, DVD)
- Transcodes in place using GPU H.265
- Keeps all English audio tracks
- Creates output file with same name
- Returns success/fail status

### 3. move_completed.py
- Takes transcoded file path as argument
- Moves file to media/movies folder
- Deletes original MKV file
- Only runs if transcode was successful

### 4. handle_failed.py
- Takes failed file path as argument
- Creates staging/failed folder if needed
- Moves both original and partial transcode to failed folder

### 5. process_queue.py
- Reads queue.txt
- For each file: calls transcode_movie.py
- If success: calls move_completed.py
- If fail: calls handle_failed.py
- Updates queue after each file

### 6. logger.py
- Logging module used by all scripts
- Writes to log folder
- Rotates logs to prevent huge files
- Provides consistent log format

### 7. config.yaml
- Contains all paths (staging, media, failed, logs)
- Contains encoding presets for blu-ray 4K, blu-ray 1080p, and DVD sources
- Single configuration file for entire pipeline

## System Information

### Hardware
- CPU: AMD Ryzen 7 3700X (8 cores, 16 threads)
- GPU: NVIDIA GeForce GTX 1660 SUPER (6GB)
- RAM: 16GB
- Storage: 931GB NVMe + 1.8TB HDD
- Network: Gigabit ethernet to NAS

### Software
- OS: Linux Mint 22.1
- Kernel: 6.8.0-60-generic
- NVIDIA Driver: 570.133.07
- HandBrake CLI: installed
- Python: 3.12.3
- mediainfo: installed
- ffmpeg/ffprobe: installed

### Key Paths
- NAS staging: /mnt/nas/data/staging
- NAS media: /mnt/nas/data/media/movies

- Alternative: /home/kevin/transcode (NVMe)