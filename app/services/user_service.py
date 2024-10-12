from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class UserService:
    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise ValueError("User not exist")
        return user

    @staticmethod
    def change_password(user_id, current_password, new_password, confirm_new_password):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        if not check_password_hash(user.password, current_password):
            raise ValueError("Current password is not correct")
        if new_password == current_password:
            raise ValueError("New password cannot be the same as the current password")
        if new_password != confirm_new_password:
            raise ValueError("New passwords do not match")
        # Mã hóa mật khẩu mới
        hashed_password = generate_password_hash(new_password)
        # Cập nhật mật khẩu người dùng trong cơ sở dữ liệu
        user.password = hashed_password
        db.session.commit()

        return {"message": "Password changed successfully"}

    @staticmethod
    def test_password_verification(user_id, password):
        user = User.query.get(user_id)
        if user:
            return check_password_hash(user.password, password)
        return False
