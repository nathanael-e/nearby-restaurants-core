# pylint: disable=C0103
from itsdangerous import Serializer, BadSignature, SignatureExpired
from flask import Blueprint, request, jsonify
import requests
from .. import constants


class LocationAPI:
    __BEARER = "Bearer "

    def __init__(self, app):
        self.app = app
        self.bp = Blueprint("location", __name__, url_prefix="/api/location")
        self.bp.before_request(self.__validate_token)
        self.bp.route("/restaurants", methods=["GET"])(self.__restaurants)

    def __validate_token(self):
        token = request.headers.get("Authorization")
        if token and token.startswith(self.__BEARER):
            token = token[len(self.__BEARER) :]
            serializer = Serializer(self.app.config[constants.API_TOKEN])
            try:
                serializer.loads(token)
                return None
            except SignatureExpired:
                return jsonify({"message": "Token has expired"}), 401
            except BadSignature:
                return jsonify({"message": "Invalid token"}), 401
        else:
            return jsonify({"message": "This API requires an access token."}), 401

    def __restaurants(self):
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
            if status:
                if status == "OK":
                    return self.__parse_response(json_response)
                return jsonify("error: received invalid status code: " + status), 400
        return jsonify({"error": "Failed to fetch data"}), 500

    def __parse_response(self, response: dict):
        results = []
        for restaurant in response["results"]:
            results.append(
                {
                    "name": restaurant["name"],
                    "vicinity": restaurant["vicinity"],
                    "rating": restaurant["rating"],
                }
            )
        return jsonify({"results": results})

    def get_bp(self):
        """Return the blueprint"""
        return self.bp
