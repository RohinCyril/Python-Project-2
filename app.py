from flask import Flask
import config

from api import register_blueprints


def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)

    # Load configuration
    app.config["UPLOAD_FOLDER"] = config.UPLOAD_FOLDER
    app.config["TRANSCODED_FOLDER"] = config.TRANSCODED_FOLDER
    app.config["HLS_FOLDER"] = config.HLS_FOLDER
    app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH
    app.config["SECRET_KEY"] = config.SECRET_KEY

    # Register API blueprints
    register_blueprints(app)

    @app.route("/")
    def home():
        return {
            "message": "Video Transcoding Pipeline API",
            "status": "Running"
        }

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )