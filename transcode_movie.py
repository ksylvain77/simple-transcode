#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path
import yaml
from logger import logger
import shutil

def check_dependencies():
    # Check for mediainfo
    mediainfo_path = shutil.which('mediainfo')
    if not mediainfo_path:
        logger.error("mediainfo not found in PATH. Please install it first.")
        sys.exit(1)
    logger.info(f"Found mediainfo at: {mediainfo_path}")
    
    # Check for HandBrakeCLI
    handbrake_path = shutil.which('HandBrakeCLI')
    if not handbrake_path:
        logger.error("HandBrakeCLI not found in PATH. Please install it first.")
        sys.exit(1)
    logger.info(f"Found HandBrakeCLI at: {handbrake_path}")

def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def get_preset(source_path):
    # Run mediainfo to get source information
    cmd = ['mediainfo', '--Inform=Video;%Width%x%Height%', str(source_path)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        dimensions = result.stdout.strip()
        
        if not dimensions:
            logger.warning(f"Could not detect dimensions for {source_path}, using 4kUHD preset")
            return '4kUHD'
            
        width, height = map(int, dimensions.split('x'))
        logger.info(f"Detected source resolution: {width}x{height}")
        
        # Determine preset based on resolution
        if width >= 3840 or height >= 2160:  # 4K
            return '4kUHD'
        elif width >= 1920 or height >= 1080:  # 1080p
            return 'bluray'
        else:  # DVD or lower
            return 'dvd'
            
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running mediainfo: {e}")
        return '4kUHD'  # Default to 4kUHD on error
    except Exception as e:
        logger.error(f"Unexpected error detecting source: {e}")
        return '4kUHD'  # Default to 4kUHD on error

def transcode_file(source_path, config):
    source = Path(source_path)
    if not source.exists():
        logger.error(f"Source file not found: {source}")
        return False
    
    # Get output path (same directory, add -transcoded)
    output = source.parent / f"{source.stem}-transcoded{source.suffix}"
    
    # Get preset settings
    preset = get_preset(source)
    settings = config['presets'][preset]
    
    logger.info(f"Transcoding {source.name} using {preset} preset")
    logger.info(f"Source size: {source.stat().st_size / 1e9:.2f}GB")
    
    # Build HandBrake command
    cmd = [
        'HandBrakeCLI',
        '-i', str(source),
        '-o', str(output),
        '--encoder', settings['encoder'],
        '--quality', str(settings['quality']),
        '--encoder-preset', settings['preset'],
        '--audio-lang-list', settings['audio']['lang_list'],
        '--all-audio',
        '--aencoder', settings['audio']['encoder'],
        '--audio-fallback', settings['audio']['fallback'],
        '--format', settings['format']
    ]
    
    # Add optional settings if they exist
    if 'max_width' in settings:
        cmd.extend(['--max-width', str(settings['max_width'])])
    if 'max_height' in settings:
        cmd.extend(['--max-height', str(settings['max_height'])])
    if 'decomb' in settings:
        cmd.extend(['--decomb', settings['decomb']])
    if 'deinterlace' in settings:
        cmd.extend(['--deinterlace', settings['deinterlace']])
    
    logger.info(f"Running command: {' '.join(cmd)}")
    
    # Run HandBrake
    try:
        process = subprocess.run(cmd, check=True)
        if process.returncode == 0 and output.exists():
            logger.info(f"Transcode successful: {output.name}")
            logger.info(f"Output size: {output.stat().st_size / 1e9:.2f}GB")
            return True
        else:
            logger.error("Transcode failed")
            return False
    except subprocess.CalledProcessError as e:
        logger.error(f"HandBrake error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        logger.error("Usage: transcode_movie.py <source_file>")
        sys.exit(1)
    
    # Check dependencies first
    check_dependencies()
    
    source_path = sys.argv[1]
    config = load_config()
    
    if transcode_file(source_path, config):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main() 