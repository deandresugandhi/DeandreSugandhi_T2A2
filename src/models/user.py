
# Third-party Library Modules
from marshmallow import fields
from marshmallow.validate import Length

# Local Modules
from setup import db, ma


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    item_posts = db.relationship('ItemPost', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')

class UserSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=Length(min=8))
    item_posts = fields.Nested('ItemPostSchema', only=['id', 'title'], many=True)

    class Meta:
        fields = ("id", "name", "username", "email", "password", "is_admin", "item_posts")
