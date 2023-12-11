# Standard Library Modules
from datetime import datetime

# Third-party Library Modules
from marshmallow import fields
from marshmallow.validate import OneOf, Regexp, Length, And

# Local Modules
from setup import db, ma


VALID_CATEGORIES = (
    'electronics', 'apparel', 'computers', 
    'jewellery', 'others'
)

class ItemPost(db.Model):
    __tablename__ = "item_posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    item_type = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    item_description = db.Column(db.Text)
    retrieval_description = db.Column(db.Text)
    status = db.Column(db.String(30), nullable=False)
    date = db.Column(db.Date, default=datetime.now().strftime('%Y-%m-%d'))

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seen_location_id = db.Column(
        db.Integer,
        db.ForeignKey('locations.id'),
    )
    pickup_location_id = db.Column(
        db.Integer,
        db.ForeignKey('locations.id'),
    )

    # Relationships
    user = db.relationship('User', back_populates='item_posts')
    comments = db.relationship('Comment', back_populates='item_post')
    images = db.relationship('Image', back_populates='item_post')
    seen_location = db.relationship('Location', back_populates='item_post_seen', foreign_keys=[seen_location_id])
    pickup_location = db.relationship('Location', back_populates='item_post_pickup', foreign_keys=[pickup_location_id])


class ItemPostSchema(ma.Schema):
    title = fields.String(required=True, validate=And(
        Regexp('^[0-9a-zA-Z ]+$', error='Title must contain only letters, numbers and whitespaces'),
        Length(min=3, error='Title must be at least 3 characters long')
    ))
    status = fields.String(validate=OneOf(VALID_CATEGORIES))
    user = fields.Nested('UserSchema', only=['id', 'name', 'username'])
    comments = fields.Nested('CommentSchema', many=True, exclude=['item_post'])
    images = fields.Nested('ImageSchema', many=True, exclude=['item_post'])
    seen_location = fields.Nested('LocationSchema')
    pickup_location = fields.Nested('LocationSchema')

    class Meta:
        fields = ("id", "title", "item_type", "category", "item_description", "retrieval_description",
                  "status", "date", "user", "comments", "images", "seen_location", "pickup_location")
