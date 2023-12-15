"""
A module containing the model and schema of an item post record in the database.
"""

# Standard Library Modules
from datetime import datetime

# Third-party Library Modules
from marshmallow import fields
from marshmallow.validate import OneOf, Regexp, Length, And

# Local Modules
from setup import db, ma


# Defines what is accepted in the categories attribute of the table
VALID_CATEGORIES = (
    'electronics', 'apparel', 'computers', 
    'jewellery', 'others'
)

VALID_STATUS = (
    'unclaimed', 'claimed', 'pending'
)

VALID_POST_TYPE = (
    'lost', 'found'
)


class ItemPost(db.Model):
    """
    Creates the table structure of the "item_posts" table using SQLAlchemy.
    """
    __tablename__ = "item_posts"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Attributes
    title = db.Column(db.String(80), nullable=False)
    post_type = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    item_description = db.Column(db.Text)
    retrieval_description = db.Column(db.Text)
    status = db.Column(db.String(10), nullable=False, default='unclaimed')
    date = db.Column(db.Date, default=datetime.now().strftime('%Y-%m-%d'))

    # Foreign keys
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
    )
    seen_location_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'locations.id',
            # Set this key to NULL if referred location is deleted
            ondelete='SET NULL'
        )
    )
    pickup_location_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'locations.id',
            # Set this key to NULL if referred location is deleted
            ondelete='SET NULL'
        )
    )

    # Relationships
    user = db.relationship('User', back_populates='item_posts')
    comments = db.relationship(
        'Comment',
        back_populates='item_post',
        # Deletes or updates all its associated comments when an item post is
        # deleted or updated
        cascade='all, delete'
    )
    images = db.relationship(
        'Image',
        back_populates='item_post',
        # Deletes or updates all its associated images when an item post is
        # deleted or updated
        cascade='all, delete'
    )
    seen_location = db.relationship('Location',
        back_populates='item_post_seen',
        foreign_keys=[seen_location_id]
    )
    pickup_location = db.relationship('Location',
        back_populates='item_post_pickup',
        foreign_keys=[pickup_location_id]
    )


class ItemPostSchema(ma.Schema):
    """
    Defines the schema to convert an "item_post" record using Marshmallow
    into a readable format.
    """
    title = fields.String(required=True, validate=And(
        Regexp('^[0-9a-zA-Z -]+$', error='Title must contain only letters, numbers and whitespaces'),
        Length(min=3, error='Title must be at least 3 characters long')
    ))
    category = fields.String(required=True, validate=OneOf(VALID_CATEGORIES))
    post_type = fields.String(load_default='unclaimed', validate=OneOf(VALID_POST_TYPE))
    status = fields.String(validate=OneOf(VALID_STATUS))
    user = fields.Nested('UserSchema', only=['id', 'name', 'username'])
    comments = fields.Nested('CommentSchema', many=True, exclude=['item_post'])
    seen_location = fields.Nested('LocationSchema')
    pickup_location = fields.Nested('LocationSchema')
    images = fields.Nested('ImageSchema', many=True, exclude=['item_post', 'comment'])

    class Meta:
        ordered = True
        fields = ("id", "title", "post_type", "category", "item_description",
            "retrieval_description", "status", "date", "user", "comments",
            "seen_location", "pickup_location", "images")
