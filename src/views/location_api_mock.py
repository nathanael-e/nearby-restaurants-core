# pylint: disable=C0103,W0231,R0801
import json
import time

from flask import Blueprint, Flask, make_response, request, send_file

from .location_api import LocationAPI


class LocationAPIMock(LocationAPI):
    def __init__(
        self,
        app: Flask,
    ):
        self.app = app
        self.logger = app.logger
        self.bp = Blueprint("location", __name__, url_prefix="/api/location")
        self.bp.before_request(self._validate_token)
        self.bp.route("/restaurants", methods=["GET"])(self._restaurants)
        self.bp.route("/photo", methods=["GET"])(self._photo)

    def _restaurants(self):
        with open(
            "src/resources/mock/restaurants/restaurants_response.json",
            "r",
            encoding="utf-8",
        ) as restaurants_response:
            json_data = json.load(restaurants_response)
            response = make_response(json.dumps(json_data))
            response.headers["Content-Type"] = "application/json"
            return response

    def _photo(self):
        photo_reference = request.args.get("photo_reference")
        height = request.args.get("height")
        width = request.args.get("width")
        if not photo_reference or not height or not width:
            return "An error occured ...", 400
        if photo_reference == "1":
            return send_file(
                "resources/mock/restaurants/images/amaranten.jpg",
            )
        if photo_reference == "2":
            time.sleep(5)
            return send_file(
                "resources/mock/restaurants/images/cafe_bla.jpg",
                mimetype="image/jpeg",
            )
        if photo_reference == "3":
            return send_file(
                "resources/mock/restaurants/images/mcdonalds.jpg",
                mimetype="image/jpeg",
            )
        return "An error occured ...", 400
