"""
A module containing the model and schema of a location record in the database.
"""


# Third-party Library Modules
from marshmallow import fields, validates, ValidationError
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
    unit_number = db.Column(db.String, default="")
    street_number = db.Column(db.String, default="")
    street_name = db.Column(db.String, default="")
    suburb = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    postcode = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String, nullable=False)

    # Relationships
    item_post_seen = db.relationship('ItemPost',
        back_populates='seen_location',
        foreign_keys=[ItemPost.seen_location_id])
    item_post_pickup = db.relationship('ItemPost',
        back_populates='pickup_location',
        foreign_keys=[ItemPost.pickup_location_id])

    # Unique Constraint Combination
    __table_args__ = (
        UniqueConstraint("unit_number", "street_number", "street_name", "suburb", "state", "postcode", "country"),
    )

class LocationSchema(ma.Schema):
    """
    Defines the schema to convert a "location" record using Marshmallow into a
    readable format.
    """
    unit_number = fields.String(load_default="")
    street_number = fields.String(load_default="")
    street_name = fields.String(load_default="")
    suburb = fields.String(required=True)
    state = fields.String(required=True)
    postcode = fields.Integer(required=True)
    country = fields.String(required=True)

    # Ensures unit number is a string containing only digits
    @validates('unit_number')
    def validate_unit_number(self, value):
        if value and not value.isdigit():
            raise ValidationError('Unit number must contain only digits.')

    # Ensures street number is a string containing only digits
    @validates('street_number')
    def validate_street_number(self, value):
        if value and not value.isdigit():
            raise ValidationError('Street number must contain only digits.')

    class Meta:
        ordered = True
        fields = ("id", "unit_number", "street_number", "street_name",
                  "suburb", "state", "postcode", "country")
