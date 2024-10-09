from flask import Blueprint, request, jsonify
from ..services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    try:
        result = AuthService.register_user(username, email, password)
        return (
            jsonify(
                {
                    "message": "User registered successfully",
                    "user": result["user"].username,
                    "access_token": result["access_token"],
                    "refresh_token": result["refresh_token"],
                }
            ),
            201,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
