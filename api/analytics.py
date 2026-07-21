import os
import json
import subprocess

from flask import Blueprint, jsonify

from config import UPLOAD_FOLDER

analytics_bp = Blueprint("analytics", __name__)


def get_video_metadata(video_path):
    """
    Extract metadata using FFprobe.
    """

    command = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        video_path
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise Exception(result.stderr)

    data = json.loads(result.stdout)

    video_stream = next(
        (
            stream for stream in data["streams"]
            if stream["codec_type"] == "video"
        ),
        None
    )

    metadata = {
        "filename": os.path.basename(video_path),
        "file_size_mb": round(
            os.path.getsize(video_path) / (1024 * 1024),
            2
        ),
        "duration_seconds": float(
            data["format"].get("duration", 0)
        ),
        "bitrate": data["format"].get("bit_rate"),
        "format": data["format"].get("format_name")
    }

    if video_stream:
        metadata.update({
            "codec": video_stream.get("codec_name"),
            "resolution": (
                f"{video_stream.get('width')}x"
                f"{video_stream.get('height')}"
            ),
            "fps": video_stream.get("r_frame_rate")
        })

    return metadata


@analytics_bp.route("/analytics/<filename>", methods=["GET"])
def analytics(filename):
    """
    Return metadata of an uploaded video.
    """

    video_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(video_path):
        return jsonify({
            "success": False,
            "message": "Video not found."
        }), 404

    try:
        metadata = get_video_metadata(video_path)

        return jsonify({
            "success": True,
            "metadata": metadata
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500