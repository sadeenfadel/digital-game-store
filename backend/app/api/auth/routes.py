from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.auth import LoginSchema, LoginResponseSchema, UserSchema
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
@auth_bp.arguments(LoginSchema)
@auth_bp.response(200, LoginResponseSchema)
@auth_bp.alt_response(401, description="Invalid credentials")
def login(credentials):
    user, error, token = AuthService.authenticate(
        credentials["email"], credentials["password"]
    )
    if error:
        abort(401, message=error)
    return {"access_token": token, "user": UserSchema().dump(user)}


@auth_bp.route("/me", methods=["GET"])
@auth_bp.doc(security=[{"BearerAuth": []}])
@auth_bp.response(200, UserSchema)
@auth_bp.alt_response(401, description="Missing or invalid token")
@jwt_required()
def get_current_user():
    user_id = int(get_jwt_identity())
    from app.models.user import User
    from app.extensions import db

    user = db.session.get(User, user_id)
    if not user:
        abort(401, message="User not found.")
    return UserSchema().dump(user)
