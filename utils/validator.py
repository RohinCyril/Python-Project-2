import os
import mimetypes

from config import ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH


def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.

    Args:
        filename (str)

    Returns:
        bool
    """
    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS


def validate_file_size(file):
    """
    Validate uploaded file size.

    Args:
        file (FileStorage)

    Returns:
        bool
    """
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)

    return size <= MAX_CONTENT_LENGTH


def validate_mime_type(filename):
    """
    Validate MIME type based on filename.

    Args:
        filename (str)

    Returns:
        bool
    """
    mime_type, _ = mimetypes.guess_type(filename)

    allowed_mime_types = {
        "video/mp4",
        "video/x-msvideo",      # AVI
        "video/quicktime",      # MOV
        "video/x-matroska",     # MKV
        "video/x-ms-wmv",       # WMV
    }

    return mime_type in allowed_mime_types


def validate_upload(file):
    """
    Perform all upload validations.

    Args:
        file (FileStorage)

    Returns:
        tuple(bool, str)
    """
    if file is None:
        return False, "No file uploaded."

    if file.filename == "":
        return False, "Filename is empty."

    if not allowed_file(file.filename):
        return False, "Unsupported file extension."

    if not validate_mime_type(file.filename):
        return False, "Invalid MIME type."

    if not validate_file_size(file):
        max_size_mb = MAX_CONTENT_LENGTH // (1024 * 1024)
        return False, f"File size exceeds {max_size_mb} MB."

    return True, "Validation successful."