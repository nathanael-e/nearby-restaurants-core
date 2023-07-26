import os
from itsdangerous import Serializer
from flask import Flask
from .views import app_restfinder_info
from .views.location_api import LocationAPI


class FlaskServer:
    def __init__(self):
        self.app = Flask(__name__, instance_relative_config=True)
        api_secret = os.getenv("API_SECRET")
        if not api_secret:
            raise ValueError("Environment variable 'API_SECRET' is null")
        self.app.config["SECRET_KEY"] = api_secret
        self.__init()

    def __init(self):
        self.__create_blueprints()

    def __create_blueprints(self):
        """Create blueprints"""
        self.app.register_blueprint(app_restfinder_info.bp)
        self.app.register_blueprint(LocationAPI(self.app).get_bp())

    def get_app(self):
        """Return the flask app"""
        return self.app


def create_app():
    """Create flask and add blueprints"""
    server = FlaskServer()
    app = server.get_app()
    return app
