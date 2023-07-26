import os
import pytest
from flask import Flask
from src import FlaskServer


@pytest.fixture()
def app():
    os.environ["API_SECRET"] = "test_api_secret"
    flask_server = FlaskServer()
    app = flask_server.get_app()
    app.config.update({"TESTING": True})
    yield app


def test_app_restfinder_info(app: Flask):
    with app.test_client() as client:
        response = client.get("/")
        data = response.data.decode("utf-8")
        assert response.status_code == 200
        assert data == "Welcome ..."
