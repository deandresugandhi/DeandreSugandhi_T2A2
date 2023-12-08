from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from setup import db
from models.item_post import ItemPost, ItemPostSchema
from models.location import Location, LocationSchema
from auth import authorize

item_posts_bp = Blueprint('item_posts', __name__, url_prefix='/item-posts')

def categorize_location(raw_info):
    def register_location(raw_info, location_attribute):
        if location_attribute not in raw_info:
            return None
        location_data = raw_info[location_attribute]
        location = Location(
            street_number = location_data.get('street_number', ''),
            street_name = location_data.get('street_name', ''),
            suburb = location_data.get('suburb'),
            postcode = location_data.get('postcode'),
            country = location_data.get('country')
        )
        db.session.add(location)
        db.session.commit()

        return location

    seen_location = register_location(raw_info, 'seen_location')
    pickup_location = register_location(raw_info, 'pickup_location')

    return seen_location, pickup_location


# Get all item posts
@item_posts_bp.route("/")
@jwt_required()
def all_item_posts():
    stmt = db.select(ItemPost)
    item_posts = db.session.scalars(stmt).all()
    if item_posts:
        return ItemPostSchema(many=True).dump(item_posts)
    return {'error': 'No item posts founds'}, 404

# Get one item post
@item_posts_bp.route('/<int:id>')
@jwt_required()
def one_item_post(id):
    stmt = db.select(ItemPost).filter_by(id=id)
    item_post = db.session.scalar(stmt)
    if item_post:
        return ItemPostSchema().dump(item_post)
    return {'error': 'Item post not found'}, 404

# Create a new item post
@item_posts_bp.route('/', methods=['POST'])
@jwt_required()
def create_item_post():
    item_post_info = ItemPostSchema(exclude=['id', 'date']).load(request.json)
    seen_location, pickup_location = categorize_location(item_post_info)
    item_post = ItemPost(
        title = item_post_info['title'],
        item_type = item_post_info.get('item_type'),
        category = item_post_info.get('category'),
        item_description = item_post_info.get('item_description', ''),
        retrieval_description = item_post_info.get('retrieval_description', ''),
        status = item_post_info.get('status', 'Unclaimed'),
        user_id = get_jwt_identity(),
        seen_location_id = seen_location.id,
        pickup_location_id = pickup_location.id
    )
    db.session.add(item_post)
    db.session.commit()
    return ItemPostSchema().dump(item_post), 201

