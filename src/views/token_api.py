# pylint: disable=C0103
import datetime
import jwt
from flask import Blueprint, jsonify, Response
from .. import constants


class TokenAPI:
    def __init__(self, app):
        self.app = app
        self.bp = Blueprint("token", __name__, url_prefix="/api/token")
        self.bp.route("/renew", methods=["GET"])(self.__renew_token)

    def __renew_token(self) -> Response:
        payload = {"exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=900)}
        return (
            jsonify(
                {"token": jwt.encode(payload, self.app.config[constants.API_TOKEN])}
            ),
            200,
        )

    def get_bp(self) -> Blueprint:
        """Get the blueprint"""
        return self.bp
