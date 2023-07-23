from flask import Blueprint, request, jsonify

bp = Blueprint("location", __name__, url_prefix="/api/location")


@bp.route("/restaurants", methods=["GET"])
def restaurants():
    """Return near restaruants based on longitude and latitude"""
    longitude = request.args.get("longitude")
    altitude = request.args.get("latitude")

    if not longitude or not altitude:
        return jsonify({"error": "Both longitude and latitude are required."}), 400

    restaurants_data = [
        {"name": "Restaurant A", "longitude": 123.45, "latitude": 67.89},
        {"name": "Restaurant B", "longitude": 98.76, "latitude": 54.32},
    ]

    return jsonify(restaurants_data)
