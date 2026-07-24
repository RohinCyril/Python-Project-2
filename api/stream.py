import os

from flask import Blueprint, jsonify, send_from_directory

from config import HLS_FOLDER

stream_bp = Blueprint("stream", __name__)


@stream_bp.route("/stream/<video_name>", methods=["GET"])
def stream_playlist(video_name):
    """
    Stream the HLS playlist (.m3u8).

    Example:
    GET /api/stream/movie
    """

    playlist = os.path.join(HLS_FOLDER, video_name, "playlist.m3u8")

    if not os.path.exists(playlist):
        return jsonify({
            "success": False,
            "message": "Playlist not found. Please transcode the video first."
        }), 404

    return send_from_directory(
        os.path.join(HLS_FOLDER, video_name),
        "playlist.m3u8",
        mimetype="application/vnd.apple.mpegurl"
    )


@stream_bp.route("/stream/<video_name>/<segment>", methods=["GET"])
def stream_segment(video_name, segment):
    """
    Stream HLS .ts segments.

    Example:
    GET /api/stream/movie/segment000.ts
    """

    directory = os.path.join(HLS_FOLDER, video_name)
    segment_path = os.path.join(directory, segment)

    if not os.path.exists(segment_path):
        return jsonify({
            "success": False,
            "message": "Segment not found."
        }), 404

    return send_from_directory(
        directory,
        segment,
        mimetype="video/mp2t"
    )