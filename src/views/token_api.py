# pylint: disable=C0103
from itsdangerous import TimedSerializer
from flask import Blueprint, jsonify, Response
from .. import constants


class TokenAPI:
    def __init__(self, app):
        self.app = app
        self.serializer = TimedSerializer(self.app.config[constants.API_TOKEN])
        self.bp = Blueprint("token", __name__, url_prefix="/api/token")
        self.bp.route("/renew", methods=["GET"])(self.__renew_token)

    def __renew_token(self) -> Response:
        return jsonify({"token": self.serializer.dumps({})}), 200

    def get_bp(self) -> Blueprint:
        """Get the blueprint"""
        return self.bp
