# pylint: disable=C0103
import jwt
import requests
from flask import Blueprint, Flask, Response, jsonify, request

from .. import constants

nearby_search_template = {
    "name": constants.MAP,
    "vicinity": constants.MAP,
    "place_id": constants.MAP,
    "rating": constants.OPTIONAL,
    "photos": constants.MAP,
}

photo_keys = ["height", "width", "photo_reference"]


excluded_types = ["gas_station"]


class LocationAPI:
    __BEARER = "Bearer "

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

    def _validate_token(self):
        self.logger.info("URL: %s", request.url)
        self.logger.info("Headers: %s", request.headers)
        self.logger.info("Body: %s", request.get_data())
        token = None
        if request.headers.get("Authorization"):
            token = request.headers.get("Authorization")
            if token.startswith(self.__BEARER):
                token = token[len(self.__BEARER) :]
        elif request.args.get("token"):
            token = request.args.get("token")
        if token:
            try:
                jwt.decode(
                    token, self.app.config[constants.API_TOKEN], algorithms=["HS256"]
                )
                return None
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Token has expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Invalid token"}), 401
        else:
            return jsonify({"message": "This API requires an access token."}), 401

    def _restaurants(self):
        """Return near restaurants based on longitude and latitude"""
        longitude = request.args.get("longitude")
        latitude = request.args.get("latitude")
        if not longitude or not latitude:
            return jsonify({"error": "Both longitude and latitude are required."}), 400
        url = (
            "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
            f"location={latitude}%2C{longitude}&rankby=distance&"
            f"type=restaurant&opennow&key={self.app.config[constants.API_GOOGLE_PLACES_TOKEN]}"
        )
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            json_response = response.json()
            status = json_response["status"]
            if status == "OK":
                return self.__parse_response(json_response)
        return jsonify({"error": "Failed to fetch data"}), 500

    def _photo(self):
        photo_reference = request.args.get("photo_reference")
        height = request.args.get("height")
        width = request.args.get("width")
        if not photo_reference or not height or not width:
            return "An error occured ...", 400
        url = (
            "https://maps.googleapis.com/maps/api/place/photo"
            f"?maxwidth={width}&maxheight{height}&photo_reference={photo_reference}"
            f"&key={self.app.config[constants.API_GOOGLE_PLACES_TOKEN]}"
        )
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return Response(
                response.content, content_type=response.headers["Content-Type"]
            )
        return jsonify({"error": "An error occured. Please try again."}), 500

    def __parse_response(self, response):
        results = []
        for result in response["results"]:
            self.__add_restaurant(result, results)
        return jsonify({"results": results})

    def __add_restaurant(self, result: dict, results: list) -> None:
        if result.get("types") is None:
            return
        for place_type in result.get("types"):
            if place_type in excluded_types:
                return
        mapped_response = {}
        for key, value in nearby_search_template.items():
            success = self.__map(key, result, mapped_response)
            if value == constants.MAP and not success:
                return
        results.append(mapped_response)

    def __map(self, key: str, result: dict, mapped_response: dict) -> bool:
        if result.get(key) is None:
            return False
        if isinstance(result.get(key), list) and len(result.get(key)) == 0:
            return False
        if key == "photos":
            return self.__map_photo(result["photos"][0], mapped_response)
        mapped_response[key] = result[key]
        return True

    def __map_photo(self, photo: dict, mapped_response: dict) -> bool:
        mapped_photo = {}
        for key in photo_keys:
            if photo.get(key) is None:
                return False
            mapped_photo[key] = photo[key]
        mapped_response["photo"] = mapped_photo
        return True

    def get_bp(self):
        """Return the blueprint"""
        return self.bp
