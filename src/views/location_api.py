# pylint: disable=C0103
from itsdangerous import Serializer, BadSignature, SignatureExpired
from flask import Blueprint, request, jsonify


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
            serializer = Serializer(self.app.config["SECRET_KEY"])
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

        restaurants_data = [
            {"name": "Restaurant A", "longitude": 123.45, "latitude": 67.89},
            {"name": "Restaurant B", "longitude": 98.76, "latitude": 54.32},
        ]

        return jsonify(restaurants_data)

    def get_bp(self):
        """Return the blueprint"""
        return self.bp
