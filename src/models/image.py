"""
A module containing the model and schema of an image record in the database.
"""


# Third-party Library Modules
from marshmallow import fields

# Local Modules
from setup import db, ma


class Image(db.Model):
    """
    Creates the table structure of the "images" table using SQLAlchemy.
    """
    __tablename__ = "images"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Attributes
    image_url = db.Column(db.String, nullable=False)

    # Foreign Keys
    item_post_id = db.Column(db.Integer, db.ForeignKey('item_posts.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))

    # Relationships
    item_post = db.relationship('ItemPost', back_populates='images')
    comment = db.relationship('Comment', back_populates='images')

class ImageSchema(ma.Schema):
    """
    Defines the schema to convert a "location" record using Marshmallow into a
    readable format.
    """
    item_post = fields.Nested('ItemPostSchema', only=['id', 'title'])
    comment = fields.Nested('CommentSchema', only=['id'])

    class Meta:
        fields = ("id", "image_url", "item_post", "comment")
