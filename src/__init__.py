import os
from flask import Flask
from . import constants
from .views import app_restfinder_info
from .views.token_api import TokenAPI
from .views.location_api import LocationAPI


class FlaskServer:
    def __init__(self):
        self.app = Flask(__name__, instance_relative_config=True)
        api_secret = os.getenv(constants.API_TOKEN)
        google_places_api_sercet = os.getenv(constants.API_GOOGLE_PLACES_TOKEN)
        if not api_secret:
            raise ValueError(f"Environment variable '{constants.API_TOKEN}' is null")
        if not google_places_api_sercet:
            raise ValueError(
                f"Environment variable '{constants.API_GOOGLE_PLACES_TOKEN}' is null"
            )
        self.app.config[constants.API_TOKEN] = api_secret
        self.app.config[constants.API_GOOGLE_PLACES_TOKEN] = google_places_api_sercet
        self.__init()

    def __init(self):
        self.__create_blueprints()

    def __create_blueprints(self):
        """Create blueprints"""
        self.app.register_blueprint(app_restfinder_info.bp)
        self.app.register_blueprint(TokenAPI(self.app).get_bp())
        self.app.register_blueprint(LocationAPI(self.app).get_bp())

    def get_app(self):
        """Return the flask app"""
        return self.app


def create_app():
    """Create flask and add blueprints"""
    server = FlaskServer()
    app = server.get_app()
    return app
