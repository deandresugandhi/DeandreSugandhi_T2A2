"""
A module containing the model and schema of a user record in the database.
"""


# Third-party Library Modules
from marshmallow import fields
from marshmallow.validate import Length

# Local Modules
from setup import db, ma


class User(db.Model):
    """
    Creates the table structure of the "users" table using SQLAlchemy.
    """
    __tablename__ = "users"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Attributes
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    item_posts = db.relationship('ItemPost', back_populates='user', cascade='all, delete')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
    """
    Defines the schema to convert a "user" record using Marshmallow into a 
    readable format.
    """
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=Length(min=8))
    item_posts = fields.Nested('ItemPostSchema', only=['id', 'title'], many=True)

    class Meta:
        fields = ("id", "name", "username", "email", "password", "is_admin", "item_posts")
