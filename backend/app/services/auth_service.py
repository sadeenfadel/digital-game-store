from typing import Optional, Tuple, Any
from flask_jwt_extended import create_access_token
from app.models.user import User


class AuthService:
    @staticmethod
    def authenticate(
        email: str, password: str
    ) -> Tuple[Optional[User], Optional[str], Optional[str]]:
        user = User.query.filter_by(email=email).first()
        if not user:
            return None, "Invalid email or password.", None
        if not user.check_password(password):
            return None, "Invalid email or password.", None
        token = create_access_token(identity=str(user.id))
        return user, None, token

    @staticmethod
    def create_demo_user() -> User:
        email = "sadeenfadel@gmail.com"
        password = "sAdeen_11"
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email)
            user.set_password(password)
            from app.extensions import db

            db.session.add(user)
            db.session.commit()
        return user
