from flask import Blueprint, request, jsonify
from ..services.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username", "").strip()  # loại bỏ khoảng trắng
    email = data.get("email", "").strip()  # loại bỏ khoảng trắng
    password = data.get("password", "").strip()  # loại bỏ khoảng trắng

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required."}), 400

    try:
        result = AuthService.register_user(username, email, password)
        return (
            jsonify(
                {
                    "message": "User registered successfully",
                    "user": result["user"].username,
                }
            ),
            201,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@auth_bp.post("/login")
def login():
    data = request.get_json()
    email = data.get("email", "").strip()  # loại bỏ khoảng trắng
    password = data.get("password", "").strip()  # loại bỏ khoảng trắng
    if not email or not password:
        return jsonify({"error": "email, and password are required."}), 400
    try:
        result = AuthService.login_user(email, password)
        return jsonify(
            {
                "message": "User registered successfully",
                "user": result["user"],
                "access_token": result["access_token"],
                "refresh_token": result["refresh_token"],
            }
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    # Lấy user_id từ token
    current_user_id = get_jwt_identity()  # Lấy ID của người dùng từ token
    refresh_token = request.json.get("refresh_token")

    try:
        new_tokens = AuthService.refresh_token(current_user_id, refresh_token)
        return jsonify(new_tokens), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 401
