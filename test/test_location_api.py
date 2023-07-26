# pylint: disable=C0116
from test.test_base import TestBase
from flask import Flask


class TestLocationAPI(TestBase):
    def test_location_api_valid_token(self, app: Flask, headers: dict):
        with app.test_client() as client:
            response = client.get("/api/location/restaurants", headers=headers)
            data = response.json
            assert response.status_code == 400
            assert data["error"] == "Both longitude and latitude are required."

    def test_location_api_valid_token_missing_coordinates(self, app: Flask, headers):
        with app.test_client() as client:
            response = client.get("/api/location/restaurants", headers=headers)
            data = response.json
            assert response.status_code == 400
            assert data["error"] == "Both longitude and latitude are required."

    def test_location_api_missing_token(self, app):
        with app.test_client() as client:
            response = client.get("/api/location/restaurants")
            data = response.json
            assert response.status_code == 401
            assert data["message"] == "This API requires an access token."

    def test_location_api_invalid_token(self, app):
        invalid_header = {
            "Authorization": "Bearer invalid_token",
        }
        with app.test_client() as client:
            response = client.get("/api/location/restaurants", headers=invalid_header)
            data = response.json
            assert response.status_code == 401
            assert data["message"] == "Invalid token"
