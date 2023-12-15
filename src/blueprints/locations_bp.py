"""
A module that defines the blueprint for routes involving records in the 
"locations" table.
"""


# Third-party Library Modules
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_

# Local Modules
from setup import db
from models.location import Location, LocationSchema
from models.item_post import ItemPost, ItemPostSchema
from auth import authorize
from utilities import attach_image, clear_attached_images


locations_bp = Blueprint('locations', __name__, url_prefix='/locations')


# Searches for item posts based on location attributes
@locations_bp.route("/<string:field>/<string:keyword>")
def search_location(field, keyword):
    if field in ('suburb', 'state', 'postcode', 'country'):
        field = getattr(Location, field.lower())
        # Selects item posts based on the field and keyword params from URI query
        stmt = db.select(Location).filter(field.ilike(f"%{keyword}%"))
        locations = db.session.scalars(stmt).all()
        # Returns the matching item posts, or error if none are found
        if locations:
            search_id = []
            for location in locations:
                search_id.append(location.id)
            stmt = db.select(ItemPost).filter(
                or_(ItemPost.seen_location_id.in_(search_id)),
                (ItemPost.pickup_location_id.in_(search_id))
            )
            item_posts = db.session.scalars(stmt).all()
            return ItemPostSchema(many=True).dump(item_posts)
        return {'error': 'No item posts founds'}, 404
    else:
        return {'error': 'Invalid field'}, 404