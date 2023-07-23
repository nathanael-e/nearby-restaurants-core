from flask import Flask
from . import location

app = Flask(__name__, instance_relative_config=True)


def create_app():
    """Create flask and add blueprints"""
    app.register_blueprint(location.bp)
    return app
