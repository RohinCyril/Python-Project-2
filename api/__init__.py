from .upload import upload_bp
from .transcode import transcode_bp
from .stream import stream_bp
from .analytics import analytics_bp


def register_blueprints(app):
    """
    Register all API blueprints with the Flask application.
    """
    app.register_blueprint(upload_bp)
    app.register_blueprint(transcode_bp)
    app.register_blueprint(stream_bp)
    app.register_blueprint(analytics_bp)