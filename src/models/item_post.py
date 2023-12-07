from setup import db, ma
from datetime import datetime
from marshmallow import fields
from marshmallow.validate import OneOf


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
        nullable=False
    )
    pickup_location_id = db.Column(
        db.Integer,
        db.ForeignKey('locations.id'),
        nullable=False
    )

    # SQLAlchemy relationship - nests an instance of a User model in this one
    user = db.relationship('User', back_populates='cards')
    comments = db.relationship('Comment', back_populates='card')

class ItemPostSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['id', 'username'])
    comments = fields.Nested('CommentSchema', many=True, exclude=['item_post'])
    images = fields.Nested('ImageSchema', many=True, exclude=['item_post'])
    seen_location = fields.Nested('LocationSchema')
    pickup_location = fields.Nested('LocationSchema')

    class Meta:
        fields = ("id", "title", "item_type", "category", "item_description", "retrieval_description",
                  "status", "date", "user", "seen_location", "pickup_location")
