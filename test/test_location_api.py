# pylint: disable=C0116
import json
import re
from test.test_base import TestBase

import requests_mock
from flask import Flask


class TestLocationAPI(TestBase):
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

    def test_location_api_invalid_google_access_token(
        self, test_client: Flask.test_client, headers: dict
    ):
        with requests_mock.Mocker() as mocker:
            with open(
                "test/resources/google_places_invalid_access_token.json",
                encoding="utf-8",
            ) as response_json:
                mocker = requests_mock.Mocker()
                matcher = re.compile(
                    "https://maps.googleapis.com/maps/api/place/nearbysearch/.*"
                )
                mocker.get(
                    matcher,
                    json=json.load(response_json),
                )
                mocker.start()
                response = test_client.get(
                    "/api/location/restaurants?longitude=2&latitude=5",
                    headers=headers,
                )
                data = response.json
                assert response.status_code == 500
                assert data["error"] == "Failed to fetch data"

    def test_location_api_bad_request_google_api(
        self, test_client: Flask.test_client, headers: dict
    ):
        with requests_mock.Mocker() as mocker:
            mocker = requests_mock.Mocker()
            matcher = re.compile(
                "https://maps.googleapis.com/maps/api/place/nearbysearch/.*"
            )
            mocker.get(matcher, status_code=400)
            mocker.start()
            response = test_client.get(
                "/api/location/restaurants?longitude=2&latitude=5",
                headers=headers,
            )
            assert response.status_code == 500

    def test_location_api_valid_google_token(
        self, test_client: Flask.test_client, headers: dict
    ):
        with requests_mock.Mocker() as mocker:
            with open(
                "test/resources/google_places_response.json",
                encoding="utf-8",
            ) as response_json:
                mocker = requests_mock.Mocker()
                matcher = re.compile(
                    "https://maps.googleapis.com/maps/api/place/nearbysearch/.*"
                )
                mocker.get(
                    matcher,
                    json=json.load(response_json),
                )
                mocker.start()
                response = test_client.get(
                    "/api/location/restaurants?longitude=2&latitude=5",
                    headers=headers,
                )
                assert response.status_code == 200

    def test_location_api_invalid_token(self, app):
        invalid_header = {
            "Authorization": "Bearer invalid_token",
        }
        with app.test_client() as client:
            response = client.get("/api/location/restaurants", headers=invalid_header)
            data = response.json
            assert response.status_code == 401
            assert data["message"] == "Invalid token"

    def test_search_result_with_missing_attributes_are_omitted(
        self, test_client: Flask.test_client, headers: dict
    ):
        with requests_mock.Mocker() as mocker:
            with open(
                "test/resources/google_places_repsonse_mandatory_attributes_missing.json",
                encoding="utf-8",
            ) as response_json:
                mocker = requests_mock.Mocker()
                matcher = re.compile(
                    "https://maps.googleapis.com/maps/api/place/nearbysearch/.*"
                )
                mocker.get(
                    matcher,
                    json=json.load(response_json),
                )
                mocker.start()
                response = test_client.get(
                    "/api/location/restaurants?longitude=2&latitude=5",
                    headers=headers,
                )
                data = response.json
                assert response.status_code == 200
                assert data == {"results": []}
