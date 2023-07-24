from flask import Flask
from .views import app_restfinder_info, location_api


def create_app():
    """Create flask and add blueprints"""
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(app_restfinder_info.bp)
    app.register_blueprint(location_api.bp)
    return app
