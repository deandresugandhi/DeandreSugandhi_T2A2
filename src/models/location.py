# Third-party Library Modules
from marshmallow import fields
from sqlalchemy import UniqueConstraint

# Local Modules
from setup import db, ma


class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)

    street_number = db.Column(db.Integer)
    street_name = db.Column(db.String)
    suburb = db.Column(db.String, nullable=False)
    postcode = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String, nullable=False)

    # Relationships
    item_post_seen = db.relationship('ItemPost', back_populates='seen_location', foreign_keys=[ItemPost.seen_location_id])
    pickup_location = db.relationship('Location', back_populates='item_post_pickup', foreign_keys=[ItemPost.pickup_location_id])

    # Unique Constraint Combination
    _table_args__ = (
        UniqueConstraint('street_number', 'street_name', 'suburb', 'postcode', 'country'),
    )

class LocationSchema(ma.Schema):
    class Meta:
        fields = ("id", "street_number", "street_name", "suburb", "postcode", "country")
