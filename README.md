# AVI to MP4 Converter

A cross-platform utility to easily convert AVI video files to MP4 format using mplayer and ffmpeg.

## Overview

This utility is designed to help users who experience issues with AVI video files by converting them to the more widely supported MP4 format. It's specifically designed to be easy to use for people who aren't technically savvy while still providing robust functionality for advanced users.

## Features

- **Works on All Major Platforms**: Windows, macOS, and Linux support with the same code
- **User-Friendly Interface**: Simple command line interface with clear, color-coded output
- **Recursive File Finding**: Automatically finds all AVI files in a directory and its subdirectories
- **Efficient Conversion**: Uses mplayer to extract the video stream and ffmpeg to create the MP4 container
- **Progress Tracking**: Shows clear progress indicators for each step of the conversion process
- **Detailed Reporting**: Provides a summary of successful and failed conversions
- **Intelligent Error Handling**: Continues processing even if some files fail to convert
- **Helpful Guidance**: Provides platform-specific installation instructions if dependencies are missing

## Requirements

- Python 3.6 or newer
- mplayer
- ffmpeg

## Installation

### 1. Install Python 3

- **Windows**: Download and install from [python.org](https://www.python.org/downloads/windows/)
- **macOS**: 
  ```
  brew install python
  ```
- **Linux**: Usually pre-installed, or install with your package manager:
  ```
  sudo apt install python3  # Ubuntu/Debian
  sudo dnf install python3  # Fedora
  ```

### 2. Install mplayer and ffmpeg

- **Windows** (using [Chocolatey](https://chocolatey.org/)):
  ```
  choco install mplayer ffmpeg
  ```

- **macOS** (using [Homebrew](https://brew.sh/)):
  ```
  brew install mplayer ffmpeg
  ```

- **Linux**:
  ```
  sudo apt install mplayer ffmpeg  # Ubuntu/Debian
  sudo dnf install mplayer ffmpeg  # Fedora
  sudo pacman -S mplayer ffmpeg    # Arch Linux
  ```

### 3. Download the Script

Download `convert_avi_to_mp4.py` from this repository.

## Usage

### Basic Usage

```
python convert_avi_to_mp4.py [directory_path]
```

If no directory is specified, the script will use the current directory.

### Examples

```bash
# Convert AVI files in the current directory
python convert_avi_to_mp4.py

# Convert AVI files in a specific directory
python convert_avi_to_mp4.py C:\Users\username\Videos
python convert_avi_to_mp4.py /home/username/Videos
python convert_avi_to_mp4.py ~/Videos

# On macOS/Linux, you can make it executable first
chmod +x convert_avi_to_mp4.py
./convert_avi_to_mp4.py ~/Videos
```

## How It Works

1. The script searches for all AVI files in the specified directory (and subdirectories)
2. For each AVI file:
   - It uses mplayer to extract the H.264 video stream to a temporary file
   - It uses ffmpeg to wrap the H.264 stream in an MP4 container
   - The MP4 file is saved in the same location as the original AVI file
3. Temporary files are automatically cleaned up
4. A summary report is displayed showing successful and failed conversions

## Troubleshooting

If the script fails to run or convert files, check the following:

1. **Python Installation**: Ensure Python 3.6+ is installed
   ```
   python --version
   ```

2. **Required Programs**: Verify mplayer and ffmpeg are installed
   ```
   # On Windows
   where mplayer
   where ffmpeg
   
   # On macOS/Linux
   which mplayer
   which ffmpeg
   ```

3. **File Permissions**: Make sure you have read/write permissions in the target directory

4. **Video Format**: Some AVI files might use uncommon codecs that require additional parameters

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This tool uses [mplayer](http://www.mplayerhq.hu/) and [ffmpeg](https://ffmpeg.org/), which are excellent open-source media tools
