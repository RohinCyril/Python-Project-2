import os

from flask import Blueprint
from flask import request
from flask import jsonify
from werkzeug.utils import secure_filename

from config import UPLOAD_FOLDER
from utils.file_handler import save_uploaded_file

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": "No file provided."
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "success": False,
            "message": "Filename is empty."
        }), 400

    filename = secure_filename(file.filename)

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    save_uploaded_file(file, filepath)

    return jsonify({
        "success": True,
        "filename": filename,
        "location": filepath
    }), 200