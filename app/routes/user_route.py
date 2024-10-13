from flask import Blueprint, jsonify, request
from ..services.user_service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity


user_bp = Blueprint("user", __name__, url_prefix="/api/v1/user")


@user_bp.get("/me")
@jwt_required()
def me():
    try:
        current_user_id = get_jwt_identity()
        user = UserService.get_user_by_id(current_user_id)
        return jsonify(
            {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "ava_url": user.avatar_url,
                }
            }
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@user_bp.put("/change-password")
@jwt_required()
def change_password():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        if (
            not data
            or "current_password" not in data
            or "new_password" not in data
            or "confirm_new_password" not in data
        ):
            return (
                jsonify(
                    {
                        "message": "Current password, new password, and confirm new password are required"
                    }
                ),
                400,
            )

        current_password = data["current_password"]
        new_password = data["new_password"]
        confirm_new_password = data["confirm_new_password"]
        result = UserService.change_password(
            current_user_id, current_password, new_password, confirm_new_password
        )
        return jsonify(result), 200
    except ValueError as e:
        print(f"Error occurred: {str(e)}")  # In ra thông báo lỗi chi tiết
        return jsonify({"error": str(e)}), 400
