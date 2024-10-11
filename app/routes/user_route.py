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
