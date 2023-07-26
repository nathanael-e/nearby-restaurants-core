import os
import pytest
from src import FlaskServer


class TestBase:
    @pytest.fixture()
    def app(self):
        """Yeilds a test server"""
        os.environ["API_SECRET"] = "test_api_secret"
        flask_server = FlaskServer()
        app = flask_server.get_app()
        app.config.update({"TESTING": True})
        yield app

    @pytest.fixture()
    def token(self):
        """Token to be used for authentication with the test server"""
        return "{}.TZpMgVQVA5Gla6Mzrl1X2svmeCQ"

    @pytest.fixture()
    def headers(self, token):
        """Returns the HTTP header"""
        headers = {
            "Authorization": f"Bearer {token}",
        }
        return headers
