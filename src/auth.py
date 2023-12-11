"""
A module that defines how authorization works, based on JWT identity as users
login into the app.
"""


from flask import abort
from flask_jwt_extended import get_jwt_identity
from models.user import User
from setup import db

def authorize(user_id=None):
    jwt_user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=jwt_user_id)
    user = db.session.scalar(stmt)
    if not (user.is_admin or jwt_user_id == user_id):
        abort(401)
