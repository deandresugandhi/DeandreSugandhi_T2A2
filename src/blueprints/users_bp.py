"""
A module that defines the blueprint for routes involving records in the 
"users" table.
"""

# Standard Library Modules
from datetime import timedelta

# Third-party Library Modules
from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required

# Local Modules
from models.user import User, UserSchema
from setup import bcrypt, db
from auth import authorize


users_bp = Blueprint('users', __name__, url_prefix='/users')


# Allows the registration of a user account
@users_bp.route("/register", methods=["POST"])
def register():
    try:
        # Parses incoming POST user data through the UserSchema
        user_info = UserSchema(exclude=["id", "is_admin", "item_posts"]).load(request.json)
        # Create a new user record with the parsed data
        user = User(
            name=user_info["name"],
            username=user_info["username"],
            email=user_info["email"],
            password=bcrypt.generate_password_hash(user_info["password"]).decode(
                "utf8"
            ),
            private_email = user_info.get("private_email", False)
        )

        # Add and commit the new user to the database
        db.session.add(user)
        db.session.commit()

        # Returns serialized information on the new user without password and 
        # admin rights
        return UserSchema(exclude=["password", "is_admin"]).dump(user), 201
    # If username or email already exists, return error
    except IntegrityError:
        return {"error": "Username or email address already in use"}, 409


# Allows users to login to their account using either their username or email
@users_bp.route("/login", methods=["POST"])
def login():
    # Get either username or email from the POST body
    user_info = UserSchema(only=['username', 'email', 'password']).load(request.json, partial=True)
    username_or_email = user_info.get("username") or user_info.get("email")
    # Checks if user provided either a username or email
    if username_or_email:
        # Finds a user record in the db matching either the username or email
        stmt = (
            db.select(User).where(
                (User.username == username_or_email) | (User.email == username_or_email)
            )
        )
        user = db.session.scalar(stmt)
    else:
        return {"error": "Username or email is required"}, 400
    # Checks if password hash matches the specified user in the db
    if user and bcrypt.check_password_hash(user.password, request.json["password"]):
        # Create and return a JWT token + logged in user serialized information if
        # password hash matches
        token = create_access_token(identity=user.id, expires_delta=timedelta(hours=2))
        return {'token': token, 'user': UserSchema(exclude=['password', 'is_admin', 'item_posts']).dump(user)}, 202
    # Returns error if password does not match
    else:
        return {"error": "Invalid email, username, or password"}, 401


# Allows users to view all users
@users_bp.route("/")
@jwt_required()
def all_users():
    # Select all users in the db
    stmt = db.select(User)
    users = db.session.scalars(stmt).all()
    # Return all users, or error if no users are found
    if users:
        # Return serialized information on all users except passwords
        return UserSchema(many=True, exclude=['password']).dump(users), 200
    return {'error': 'No users found'}, 404


# Allows users to view specified user
@users_bp.route('/<int:id>')
@jwt_required()
def one_user(id):
    # Select user that matches the specified id
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    # Returns the user, or error if the user is not found
    if user:
         # Returns serialized user information except password
         return UserSchema(exclude=['password']).dump(user), 200
    return {'error': 'User not found'}, 404


# Allows users and admin to edit user details
@users_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user(id):
    # Parses incoming PUT or PATCH request body through the UserSchema
    user_info = UserSchema().load(request.json, partial=True)
    # Select a user record from the db that matches the id specified in the URL
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        # Only authorized users and admin can proceed to edit the details
        authorize(user.id)
        try:
            for field, value in user_info.items():
                # Edits name, username, privacy setting, and/or email information of user
                if field in ['name', 'username', 'email', 'private_email']:
                    setattr(user, field, value)
                # Hashes the new password if password is updated
                elif field == 'password':
                    user.password = bcrypt.generate_password_hash(value).decode('utf8')
                # Only admins are allowed to edit admin rights
                elif field == 'is_admin':
                    authorize()
                    user.is_admin = value
            db.session.commit()
            # Return serialized user information except password
            return UserSchema(exclude=['password']).dump(user), 201
        # IntegrityError is raised if username / email is not unique to the record,
        # and handled appropriately
        except IntegrityError:
            return {'error': 'Username or email already in use'}
    else:
        return {'error': 'User not found'}, 404


# Allows admin to delete user, alongside all information associated with them
@users_bp.route("/<int:user_id>", methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    # Select user that matches the specified id
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        # Only the user itself or admin can delete the user
        authorize(user.id)
        db.session.delete(user)
        db.session.commit()
        return {}, 200
    else:
        return {'error': 'User not found'}, 404
