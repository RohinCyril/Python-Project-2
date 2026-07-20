import os

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Directories
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
TRANSCODED_FOLDER = os.path.join(BASE_DIR, "transcoded")
HLS_FOLDER = os.path.join(BASE_DIR, "hls")

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSCODED_FOLDER, exist_ok=True)
os.makedirs(HLS_FOLDER, exist_ok=True)

# Maximum upload size (2 GB)
MAX_CONTENT_LENGTH = 2 * 1024 * 1024 * 1024

# Allowed video file extensions
ALLOWED_EXTENSIONS = {
    "mp4",
    "mov",
    "avi",
    "mkv",
    "wmv"
}

# Allowed MIME types
ALLOWED_MIME_TYPES = {
    "video/mp4",
    "video/quicktime",      # MOV
    "video/x-msvideo",      # AVI
    "video/x-matroska",     # MKV
    "video/x-ms-wmv"        # WMV
}

# FFmpeg executable
FFMPEG_BINARY = "ffmpeg"

# Thumbnail settings
THUMBNAIL_TIME = "00:00:05"

# Transcoding resolutions
VIDEO_RESOLUTIONS = {
    "720p": "1280:720",
    "480p": "854:480"
}

# Flask configuration
SECRET_KEY = "your-secret-key"

DEBUG = True
HOST = "0.0.0.0"
PORT = 5000