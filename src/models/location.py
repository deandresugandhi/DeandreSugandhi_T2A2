"""
A module containing the model and schema of a location record in the database.
"""


# Third-party Library Modules
from marshmallow import fields
from sqlalchemy import UniqueConstraint

# Local Modules
from setup import db, ma
from models.item_post import ItemPost


class Location(db.Model):
    """
    Creates the table structure of the "locations" table using SQLAlchemy.
    """
    __tablename__ = "locations"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Attributes
    street_number = db.Column(db.Integer)
    street_name = db.Column(db.String)
    suburb = db.Column(db.String, nullable=False)
    postcode = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String, nullable=False)

    # Relationships
    item_post_seen = db.relationship('ItemPost', back_populates='seen_location', foreign_keys=[ItemPost.seen_location_id])
    item_post_pickup = db.relationship('ItemPost', back_populates='pickup_location', foreign_keys=[ItemPost.pickup_location_id])

    # Unique Constraint Combination
    _table_args__ = (
        UniqueConstraint('street_number', 'street_name', 'suburb', 'postcode', 'country'),
    )

class LocationSchema(ma.Schema):
    """
    Defines the schema to convert a "location" record using Marshmallow into a
    readable format.
    """
    suburb = fields.String(required=True)
    postcode = fields.Integer(required=True)
    country = fields.String(required=True)
    class Meta:
        fields = ("id", "street_number", "street_name", "suburb", "postcode", "country")
