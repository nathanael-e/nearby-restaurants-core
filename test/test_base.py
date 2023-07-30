import os
import pytest
from flask import Flask
from src import FlaskServer


class TestBase:
    @pytest.fixture()
    def app(self):
        """Yeilds a test server"""
        os.environ["API_TOKEN"] = "test_api_secret"
        os.environ["API_GOOGLE_PLACES_TOKEN"] = "test_api_secret"
        flask_server = FlaskServer()
        app = flask_server.get_app()
        app.config.update({"TESTING": True})
        yield app

    @pytest.fixture()
    def test_client(self, app: Flask):
        """Return the test client"""
        yield app.test_client()

    @pytest.fixture()
    def token(self, test_client: Flask.test_client):
        """Token to be used for authentication with the test server"""
        return test_client.get("/api/token/renew").json["token"]

    @pytest.fixture()
    def headers(self, token):
        """Returns the HTTP header"""
        headers = {
            "Authorization": f"Bearer {token}",
        }
        return headers
