"""
A module that defines the blueprint for routes involving records in the 
"locations" table.
"""


# Third-party Library Modules
from flask import Blueprint

# Local Modules
from setup import db
from models.location import Location
from models.item_post import ItemPost, ItemPostSchema


locations_bp = Blueprint('locations', __name__, url_prefix='/locations')


# Searches for item posts based on seen location attribute
@locations_bp.route("<string:seen_or_pickup>/<string:field>/<string:keyword>")
def search_location(seen_or_pickup, field, keyword):
    # Checks if field is searchable
    if field.lower() in ('suburb', 'state', 'postcode', 'country'):
        field = getattr(Location, field.lower())
        # Selects records from the locations table matching the keyword
        stmt = db.select(Location).filter(field.ilike(f"%{keyword}%"))
        locations = db.session.scalars(stmt).all()
        if locations:
            # Gets all location id from the retrieved location records
            search_id = []
            for location in locations:
                search_id.append(location.id)
            # Gets all item posts with the gathered location id
            match seen_or_pickup:
                case "seen":
                    # Searches for item post based on seen location if
                    # seen_or_pickup is "seen"
                    stmt = db.select(ItemPost).filter(
                        ItemPost.seen_location_id.in_(search_id)
                    )
                case "pickup":
                    # Searches for item post based on pickup location if
                    # seen_or_pickup is "pickup"
                    stmt = db.select(ItemPost).filter(
                        ItemPost.pickup_location_id.in_(search_id)
                    )
                case _:
                    return {'error': 'Invalid URL'}, 404
            item_posts = db.session.scalars(stmt).all()
            # Returns serialized information on item posts matching search query
            return ItemPostSchema(many=True).dump(item_posts), 200
        return {'error': 'No item posts found'}, 404
    else:
        return {'error': 'Invalid field'}, 404
