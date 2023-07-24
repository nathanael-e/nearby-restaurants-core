from flask import Flask
from . import location, hello


def create_app():
    """Create flask and add blueprints"""
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(hello.bp)
    app.register_blueprint(location.bp)
    return app
