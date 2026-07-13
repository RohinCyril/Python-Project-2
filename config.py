import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

CHUNK_SIZE = 1024 * 1024      # 1 MB

MAX_CONTENT_LENGTH = 5 * 1024 * 1024 * 1024   # 5 GB