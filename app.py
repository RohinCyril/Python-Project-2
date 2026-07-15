from flask import Flask

from config import UPLOAD_FOLDER
from config import MAX_CONTENT_LENGTH

from routes.upload import upload_bp

import os

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.register_blueprint(upload_bp)


@app.route("/")
def home():

    return {
        "message": "Large File Upload API"
    }


if __name__ == "__main__":
    app.run(debug=True)