"""
A module that defines how authorization works, based on JWT identity as users
login into the app.
"""


from flask import abort
from flask_jwt_extended import get_jwt_identity
from models.user import User
from setup import db

def authorize(*user_ids):
    """
    Authorizes the user currently logged in before proceeding with the 
    functionality. The user currently logged in must have an id that matches
    the ids specified by the parameters to proceed.

    Args:
    1. *user_ids (int): Represents the user ids that is authorized to proceed
    """
    jwt_user_id = get_jwt_identity()

    # Abort if jwt_user_id is None or not an integer
    if jwt_user_id is None or not isinstance(jwt_user_id, int):
        abort(401)

    # Finds the user in the db with id that matches jwt_user_id
    stmt = db.select(User).filter_by(id=jwt_user_id)
    user = db.session.scalar(stmt)
    
    # Proceed if user is either an admin or id matches one of user_ids.
    # Otherwise abort.
    if not (user.is_admin or jwt_user_id in user_ids):
        abort(401)
