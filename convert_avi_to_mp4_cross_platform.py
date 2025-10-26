#!/usr/bin/env python3
"""
AVI to MP4 Converter - Cross-Platform Solution
This script converts AVI videos to MP4 format using mplayer and ffmpeg.
Works on Windows, macOS, and Linux.

Usage:
  python convert_avi_to_mp4.py [directory_path]
  
If no directory is specified, the current directory will be used.
"""

import os
import sys
import glob
import subprocess
import shutil
import tempfile
import platform
from pathlib import Path
import argparse
import time


# ANSI color codes for terminal output (will be disabled on Windows unless using a modern terminal)
class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


# Disable colors on Windows if not supported
if platform.system() == 'Windows' and not os.environ.get('WT_SESSION'):  # Check for Windows Terminal
    for attr in dir(Colors):
        if not attr.startswith('__'):
            setattr(Colors, attr, '')


def print_colored(color, message):
    """Print colored text that works across platforms"""
    print(f"{color}{message}{Colors.NC}")


def check_requirements():
    """Check if required programs are installed"""
    missing_programs = []

    # Function to check if a command exists
    def is_tool(name):
        try:
            # Check command existence differently based on platform
            if platform.system() == 'Windows':
                # On Windows, use where command (similar to Unix which)
                subprocess.run(['where', name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            else:
                # On Unix-like systems, use which command
                subprocess.run(['which', name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True
        except subprocess.SubprocessError:
            return False

    if not is_tool('mplayer'):
        missing_programs.append('mplayer')

    if not is_tool('ffmpeg'):
        missing_programs.append('ffmpeg')

    if missing_programs:
        print_colored(Colors.RED, "Error: The following required programs are not installed:")
        for program in missing_programs:
            print(f"  - {program}")

        print_colored(Colors.YELLOW, "Please install them using your system's package manager:")
        print_colored(Colors.BLUE, "For Windows (using Chocolatey):")
        print(f"  choco install {' '.join(missing_programs)}")
        print_colored(Colors.BLUE, "For macOS (using Homebrew):")
        print(f"  brew install {' '.join(missing_programs)}")
        print_colored(Colors.BLUE, "For Ubuntu/Debian:")
        print(f"  sudo apt-get install {' '.join(missing_programs)}")

        print("\nYou can download these programs from:")
        print("  - MPlayer: http://www.mplayerhq.hu/design7/dload.html")
        print("  - FFmpeg: https://ffmpeg.org/download.html")

        return False

    return True


def find_avi_files(directory):
    """Find all AVI files in the specified directory (case insensitive)"""
    # Using Path.glob for better cross-platform compatibility
    path = Path(directory)
    avi_files = list(path.glob('**/*.[aA][vV][iI]'))
    return [str(file) for file in avi_files]


def convert_avi_to_mp4(avi_file, temp_dir, remove_original_file=False):
    """Convert a single AVI file to MP4"""
    # Get file information
    file_path = Path(avi_file)
    filename = file_path.name
    base_name = file_path.stem
    output_mp4 = str(file_path.with_suffix('.mp4'))

    print_colored(Colors.YELLOW, f"Processing: {filename}")

    # Create temporary file paths
    temp_h264 = os.path.join(temp_dir, f"{base_name}.h264")

    # Step 1: Extract H.264 stream using mplayer
    print_colored(Colors.BLUE, "  Step 1/3: Extracting video stream with mplayer...")

    try:
        # Build the command differently based on platform for better compatibility
        mplayer_cmd = ['mplayer', '-dumpvideo', '-dumpfile', temp_h264, avi_file]

        # Run mplayer with output redirected
        process = subprocess.run(
            mplayer_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if process.returncode != 0 or not os.path.exists(temp_h264):
            print_colored(Colors.RED, f"  Failed to extract video stream from: {filename}")
            print_colored(Colors.RED, f"  Error: {process.stderr}")
            return False

    except Exception as e:
        print_colored(Colors.RED, f"  Error running mplayer: {str(e)}")
        return False

    # Step 2: Create MP4 container with ffmpeg
    print_colored(Colors.BLUE, "  Step 2/3: Creating MP4 with ffmpeg...")

    try:
        ffmpeg_cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error',
                      '-i', temp_h264, '-c:v', 'copy', output_mp4]

        process = subprocess.run(
            ffmpeg_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if process.returncode != 0 or not os.path.exists(output_mp4):
            print_colored(Colors.RED, f"  Failed to create MP4 file for: {filename}")
            print_colored(Colors.RED, f"  Error: {process.stderr}")
            return False

    except Exception as e:
        print_colored(Colors.RED, f"  Error running ffmpeg: {str(e)}")
        return False

    # Step 3: Verify the file was created and get its size
    print_colored(Colors.BLUE, "  Step 3/3: Verifying output file...")

    try:
        # Get file size in a readable format
        size_bytes = os.path.getsize(output_mp4)
        size_display = format_file_size(size_bytes)

        print_colored(Colors.GREEN, f"  Successfully created: {output_mp4} ({size_display})")

        # Check if we should remove the original file
        if remove_original_file:
            os.remove(avi_file)

        return True

    except Exception as e:
        print_colored(Colors.RED, f"  Error verifying output file: {str(e)}")
        return False


def format_file_size(size_in_bytes):
    """Format file size to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0 or unit == 'GB':
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Convert AVI videos to MP4 format')
    parser.add_argument('directory', nargs='?', default=os.getcwd(),
                        help='Directory containing AVI files (default: current directory)')
    parser.add_argument('--remove_original_file', nargs='?', default=False,
                        help='Deletes original file(s) if fixing them worked, (default: False)')
    args = parser.parse_args()

    target_dir = args.directory

    # Show a welcome message
    print_colored(Colors.YELLOW, "AVI to MP4 Converter - Cross-Platform")
    print(f"Running on: {platform.system()} {platform.release()}")
    print()

    # Check if the directory exists
    if not os.path.isdir(target_dir):
        print_colored(Colors.RED, f"Error: Directory '{target_dir}' does not exist.")
        return 1

    # Check for required programs
    if not check_requirements():
        return 1

    # Create a temporary directory for processing
    with tempfile.TemporaryDirectory() as temp_dir:
        print_colored(Colors.BLUE, f"Created temporary directory: {temp_dir}")

        # Find all AVI files in the directory
        print_colored(Colors.YELLOW, f"Searching for AVI files in: {target_dir}")
        avi_files = find_avi_files(target_dir)

        # Check if any AVI files were found
        if not avi_files:
            print_colored(Colors.RED, "No AVI files found in the specified directory.")
            return 0

        print_colored(Colors.GREEN, f"Found {len(avi_files)} AVI files to convert.")
        print()

        # Process each AVI file
        successful = 0
        failed = 0

        start_time = time.time()

        for avi_file in avi_files:
            if convert_avi_to_mp4(avi_file, temp_dir, args.remove_original_file):
                successful += 1
            else:
                failed += 1
            print()

        elapsed_time = time.time() - start_time

        # Show summary
        print_colored(Colors.YELLOW, "Conversion Summary:")
        print(f"  Total AVI files found: {len(avi_files)}")
        print_colored(Colors.GREEN, f"  Successfully converted: {successful}")

        if failed > 0:
            print_colored(Colors.RED, f"  Failed conversions: {failed}")

        print(f"  Total time: {elapsed_time:.2f} seconds")

        if successful > 0:
            print_colored(Colors.GREEN, "Conversion complete! Your MP4 files are in the same location as the original AVI files.")
        else:
            print_colored(Colors.RED, "No files were successfully converted.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
