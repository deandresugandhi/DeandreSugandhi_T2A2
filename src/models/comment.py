"""
A module containing the model and schema of a comment record in the database.
"""

# Standard Library Modules
from datetime import datetime

# Third-party Library Modules
from marshmallow import fields

# Local Modules
from setup import db, ma


class Comment(db.Model):
    """
    Creates the table structure of the "comments" table using SQLAlchemy.
    """
    __tablename__ = "comments"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Attributes
    comment_text = db.Column(db.Text, nullable=False)
    time_stamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_post_id = db.Column(db.Integer, db.ForeignKey('item_posts.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='comments')
    item_post = db.relationship('ItemPost', back_populates='comments')
    images = db.relationship(
        'Image',
        back_populates='comment',
        # Deletes and update all its associated comments when an item post is 
        # deleted or updated
        cascade='all, delete'
    )

class CommentSchema(ma.Schema):
    """
    Defines the schema to convert a "location" record using Marshmallow into a
    readable format.
    """
    user = fields.Nested('UserSchema', only=['id', 'username'])
    item_post = fields.Nested('ItemPostSchema', only=['id'])
    images = fields.Nested('ImageSchema', many=True, exclude=['item_post', 'comment'])

    class Meta:
        ordered = True
        fields = ("id", "comment_text", "time_stamp", "user", "images", "item_post")
