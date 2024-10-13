from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from app import db
import validators
from flask import current_app
from ..constraints.user_enum import AccountStatus


class AuthService:
    @staticmethod
    def register_user(username, email, password):
        if not validators.email(email):
            raise ValueError("Email is not valid")
        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)
        # Giả sử bạn có hàm thêm người dùng vào cơ sở dữ liệu
        db.session.add(user)
        db.session.commit()

        return {
            "user": user,
        }

    @staticmethod
    def login_user(email, password):
        if not validators.email(email):
            raise ValueError("Email is not valid")
        user: User = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError("Email does not exist")
        if not check_password_hash(user.password, password):
            raise ValueError("Incorrect password")
        if user.account_status.value != AccountStatus.ACTIVE.value:
            raise ValueError("Account is not active")
        access_token = create_access_token(
            identity=user.id
        )  # Sử dụng ID người dùng làm danh tính

        refresh_token = create_refresh_token(identity=user.id)
        redis_client = current_app.redis_client
        refresh_token_expires = current_app.config["JWT_REFRESH_TOKEN_EXPIRES"]
        expires_in = int(refresh_token_expires.total_seconds())
        redis_client.set(f"refresh_token:{user.id}", refresh_token, ex=expires_in)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {"id": user.id, "username": user.username, "email": user.email},
        }

    @staticmethod
    def refresh_token(user_id, refresh_token):
        redis_client = current_app.redis_client
        stored_refresh_token = redis_client.get(f"refresh_token:{user_id}")
        if not stored_refresh_token != refresh_token:
            raise ValueError("Invalid refresh token")
        new_access_token = create_access_token(identity=user_id)
        return {"access_token": new_access_token}
