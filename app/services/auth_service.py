from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from app import db
import validators


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
        access_token = create_access_token(
            identity=user.id
        )  # Sử dụng ID người dùng làm danh tính
        refresh_token = create_refresh_token(identity=user.id)
        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
