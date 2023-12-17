"""
A module containing the model and schema of a user record in the database.
"""

# Third-party Library Modules
from marshmallow import fields, post_dump
from marshmallow.validate import Length, And, Regexp

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
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    private_email = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    item_posts = db.relationship('ItemPost',
        back_populates='user',
        cascade='all, delete'
    )
    comments = db.relationship('Comment',
        back_populates='user',
        cascade='all, delete'
    )

class UserSchema(ma.Schema):
    """
    Defines the schema to convert a "user" record using Marshmallow into a 
    readable format.
    """
    username = fields.String(
        required = True,
        validate = And(
            Length(min=5, max=20, error="Username must be between 5 and 20 characters."),
            Regexp('^[0-9a-zA-Z _]+$', error='Username must contain only letters, '
                   'numbers, whitespaces, and underscores.')
        )
    )
    email = fields.Email(required=True)
    private_email = fields.Boolean()
    password = fields.String(
        required=True,
        validate=Length(min=8, error="Password must be at least 8 characters long."),
    )
    item_posts = fields.Nested(
        'ItemPostSchema',
        only=['id', 'title', 'status', 'post_type', 'images'],
        many=True
    )

    # Makes sure email is hidden with 'PRIVATE" when serializing the response
    # when private_email is set to True
    @post_dump(pass_many=True)
    def hide_email(self, data, many, **kwargs):
        if many:
            for user_data in data:
                if user_data['private_email']:
                    user_data['email'] = 'PRIVATE'
        else:
            if data['private_email']:
                data['email'] = 'PRIVATE'

        return data

    class Meta:
        ordered = True
        fields = ("id", "name", "username", "email", "password", "is_admin", "item_posts", "private_email")
