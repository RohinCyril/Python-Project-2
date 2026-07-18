import os

from flask import Blueprint, jsonify, request

from config import UPLOAD_FOLDER, TRANSCODED_FOLDER
from utils.file_handler import file_exists, get_file_path
from utils.transcoder import transcode_video

transcode_bp = Blueprint("transcode", __name__)


@transcode_bp.route("/transcode", methods=["POST"])
def transcode():
    """
    POST /transcode

    Request Body:
    {
        "filename": "sample.mp4"
    }
    """

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is missing."
        }), 400

    filename = data.get("filename")

    if not filename:
        return jsonify({
            "success": False,
            "message": "Filename is required."
        }), 400

    if not file_exists(filename):
        return jsonify({
            "success": False,
            "message": "Video file not found."
        }), 404

    input_file = get_file_path(filename)

    output_directory = os.path.join(
        TRANSCODED_FOLDER,
        os.path.splitext(filename)[0]
    )

    try:
        result = transcode_video(
            input_file=input_file,
            output_directory=output_directory
        )

        return jsonify({
            "success": True,
            "message": "Video transcoded successfully.",
            "outputs": result
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500