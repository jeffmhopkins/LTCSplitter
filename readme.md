# LTC Video Splitter (Python)

Split a video file into separate takes based on embedded Linear Timecode (LTC) – even when the LTC is non-contiguous, resets, or uses the non-standard "half-speed" (1200 baud) mode.

Use for:
- Single long recording with multiple non-contiguous sections of LTC (my personal use case, filming multiple takes to an LTC that tracks my DAW project for multiple layers of music that rewinds the timecode and has gaps)
- Multicam shoots where the timecode generator was left in free-run
- Files generated with https://www.calvinsundaystudios.com/ltc (including the "Half Speed" option)
- Recordings with long silences or backwards-jumping timecode

Works on Windows, macOS, Linux – only requires Python + FFmpeg.

## Features

- Detects standard 2400-baud and half-speed 1200-baud LTC automatically
- Splits exactly where LTC disappears (gaps, pauses, silences)
- Discards everything that is not LTC – no empty/silent clips
- Handles backwards jumps, continuous free-run, or reset-to-zero takes
- Lossless cutting (-c copy) – instant, no re-encoding
- Verbose logging so you can see exactly what it's doing

## Installation

Install FFmpeg (if not already installed)
- Windows (conda): conda install -c conda-forge ffmpeg
- macOS: brew install ffmpeg
- Linux: sudo apt install ffmpeg

Install Python dependencies
- pip install numpy soundfile ffmpeg-python

## Usage

Basic – auto-detects 2400-baud or 1200-baud LTC
- python ltc_split.py "path/to/your_video.mp4" 30

Specify frame rate if not 30 fps
- python ltc_split.py "my_video.mp4" 29.97

## Windows Drag-and-Drop (recommended for Windows users)

- Open drag_and_drop_ltc_splitter.bat in Notepad
- Edit only these two lines at the top:batset "CONDA_ROOT=C:\Users\YOUR_USERNAME\miniconda3"
- set "SCRIPT_PATH=C:\full\path\to\ltc_split.py"(If you don’t use conda, point CONDA_ROOT to your Python or venv folder and it will still work)
- Save the file
- Drag one or more video files onto drag_and_drop_ltc_splitter.bat

- The script processes every file automatically and shows clear progress.
- Tip: Right-click the .bat → Create shortcut → drag the shortcut to your desktop or taskbar for instant access.

- Output goes to a "splits/" folder next to your video.

# Example result:
- splits/my_video_LTC_take_01_0s.mp4
- splits/my_video_LTC_take_02_38s.mp4
