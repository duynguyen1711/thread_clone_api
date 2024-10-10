from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from app import db
import validators
import redis

redis_client = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)


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
        user = User.query.filter_by(email=email).first_or_404()
        if not check_password_hash(user.password, password):
            raise ValueError("Incorrect password")
        access_token = create_access_token(
            identity=user.id
        )  # Sử dụng ID người dùng làm danh tính
        refresh_token = create_refresh_token(identity=user.id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {"id": user.id, "username": user.username, "email": user.email},
        }
