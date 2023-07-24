from flask import Blueprint

bp = Blueprint("hello world", __name__)


@bp.route("/", methods=["GET"])
def restaurants():
    """Hello world"""
    return "Hello, world!"
