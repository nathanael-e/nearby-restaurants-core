from flask import Blueprint

bp = Blueprint("hello world", __name__)


@bp.route("/", methods=["GET"])
def hello():
    """Hello world"""
    return "Welcome ..."
