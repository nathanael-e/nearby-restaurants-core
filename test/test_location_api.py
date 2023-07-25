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


@pytest.fixture()
def token():
    return "{}.TZpMgVQVA5Gla6Mzrl1X2svmeCQ"


@pytest.fixture()
def headers(token: str):
    headers = {
        "Authorization": f"Bearer {token}",
    }
    return headers


def test_location_api_valid_token(app: Flask, headers: dict):
    with app.test_client() as client:
        response = client.get("/api/location/restaurants", headers=headers)
        data = response.json
        assert response.status_code == 400
        assert data["error"] == "Both longitude and latitude are required."


def test_location_api_valid_token_missing_coordinates(app: Flask, headers: dict):
    with app.test_client() as client:
        response = client.get("/api/location/restaurants", headers=headers)
        data = response.json
        assert response.status_code == 400
        assert data["error"] == "Both longitude and latitude are required."


def test_location_api_missing_token(app: Flask):
    with app.test_client() as client:
        response = client.get("/api/location/restaurants")
        data = response.json
        assert response.status_code == 401
        assert data["message"] == "This API requires an access token."


def test_location_api_invalid_token(app: Flask):
    invalid_header = {
        "Authorization": "Bearer invalid_token",
    }
    with app.test_client() as client:
        response = client.get("/api/location/restaurants", headers=invalid_header)
        data = response.json
        assert response.status_code == 401
        assert data["message"] == "Invalid token"
