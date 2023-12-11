"""
A module that defines the blueprint for routes involving records in the 
"item_posts" table.
"""


# Third-party Library Modules
from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError

# Local Modules
from setup import db
from models.item_post import ItemPost, ItemPostSchema
from models.location import Location, LocationSchema
from auth import authorize
from blueprints.comments_bp import comments_bp



item_posts_bp = Blueprint('item_posts', __name__, url_prefix='/item-posts')

def check_location(raw_info):
    def register_location(raw_info, location_attribute):
        if location_attribute not in raw_info:
            return None
        location_data = raw_info[location_attribute]
        location_info = LocationSchema().load(location_data)
        location = Location(**location_info)
        db.session.add(location)
        return location_info

    def retrieve_location(location_info):
        stmt = db.select(Location).filter_by(**location_info)
        location = db.session.scalar(stmt)
        return location

    try:
        seen_location_info = register_location(raw_info, 'seen_location')
        pickup_location_info = register_location(raw_info, 'pickup_location')
        db.session.commit()
    except (IntegrityError, ValidationError) as err:
        db.session.rollback()
        return {'error': err.messages}
    return retrieve_location(seen_location_info), retrieve_location(pickup_location_info)


# Get all item posts
@item_posts_bp.route("/")
def all_item_posts():
    stmt = db.select(ItemPost)
    item_posts = db.session.scalars(stmt).all()
    if item_posts:
        return ItemPostSchema(many=True).dump(item_posts)
    return {'error': 'No item posts founds'}, 404

# Get one item post
@item_posts_bp.route('/<int:id>')
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
    seen_location, pickup_location = check_location(item_post_info)
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

# Delete an item post
@item_posts_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_item_post(id):
    stmt = db.select(ItemPost).filter_by(id=id)
    item_post = db.session.scalar(stmt)
    if item_post:
        authorize(item_post.user_id)
        db.session.delete(item_post)
        db.session.commit()
        return {}, 200
    else:
        return {'error': 'Item post not found'}, 404


item_posts_bp.register_blueprint(comments_bp)