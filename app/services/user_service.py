from ..models import User
import validators


class UserService:
    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise ValueError("User not exist")
        return user
