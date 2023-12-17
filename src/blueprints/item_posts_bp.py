"""
A module that defines the blueprint for routes involving records in the 
"item_posts" table.
"""


# Third-party Library Modules
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import desc

# Local Modules
from setup import db
from models.item_post import ItemPost, ItemPostSchema
from auth import authorize
from blueprints.comments_bp import comments_bp
from blueprints.locations_bp import locations_bp
from utilities import check_location, attach_image, clear_attached_images


item_posts_bp = Blueprint('item_posts', __name__, url_prefix='/item-posts')


# Get all item posts
@item_posts_bp.route("/")
def all_item_posts():
    # Selects all item posts from the db
    stmt = db.select(ItemPost).order_by(desc('date'))
    item_posts = db.session.scalars(stmt).all()
    # Returns all item posts, or error if none are found
    if item_posts:
        return ItemPostSchema(many=True).dump(item_posts), 200
    return {'error': 'No item posts founds'}, 404


# Searches for item posts that matches certain query parameters
@item_posts_bp.route("/<string:field>/<string:keyword>")
def search_posts(field, keyword):
    if field in ('title', 'post_type', 'category', 'status', 'date'):
        field = getattr(ItemPost, field.lower())
        # Selects item posts based on the field and keyword params from URI query
        stmt = db.select(ItemPost).filter(field.ilike(f"%{keyword}%"))
        item_posts = db.session.scalars(stmt).all()
        # Returns the matching item posts, or error if none are found
        if item_posts:
            return ItemPostSchema(many=True).dump(item_posts), 200
        return {'error': 'No item posts found'}, 404
    else:
        return {'error': 'Invalid field'}, 404


# Get one item post
@item_posts_bp.route('/<int:id>')
def one_item_post(id):
    # Selects an item post from the db that matches the id
    stmt = db.select(ItemPost).filter_by(id=id)
    item_post = db.session.scalar(stmt)
    # Returns the item post, or error if the item post is not found
    if item_post:
        return ItemPostSchema().dump(item_post), 200
    return {'error': 'Item post not found'}, 404


# Create a new item post
@item_posts_bp.route('/', methods=['POST'])
@jwt_required()
def create_item_post():
    # Parses incoming POST request body through ItemPostSchema
    item_post_info = ItemPostSchema(exclude=['id', 'date', 'user', 'comments']).load(request.json)
    # Retrieve location information from parsed request
    seen_location, pickup_location = check_location(item_post_info)
    item_post = ItemPost(
        title = item_post_info['title'],
        post_type = item_post_info.get('post_type').lower(),
        category = item_post_info.get('category').lower(),
        item_description = item_post_info.get('item_description', ''),
        retrieval_description = item_post_info.get('retrieval_description', ''),
        status = item_post_info.get('status', 'unclaimed'),
        user_id = get_jwt_identity(),
        seen_location_id = seen_location.id if seen_location else None,
        pickup_location_id = pickup_location.id if pickup_location else None,
    )
    db.session.add(item_post)
    db.session.commit()

    # Create attached image records and associate them with the created item post
    attach_image(item_post_info, item_post, "item_post")

    return ItemPostSchema().dump(item_post), 201


# Edit an item post
@item_posts_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def edit_item_post(id):
    # Parses incoming POST request body through ItemPostSchema
    item_post_info = ItemPostSchema(exclude=['id', 'date', 'user', 'comments']).load(request.json, partial=True)
    # Select item post matching id params from URL query
    stmt = db.select(ItemPost).filter_by(id=id)
    item_post = db.session.scalar(stmt)
    if item_post:
        authorize(item_post.user_id)
        # Apply edit to item post
        for field, value in item_post_info.items():
            if field == 'images':
                clear_attached_images(item_post, "item_post")
                attach_image(item_post_info, item_post, "item_post")
            elif field in ['seen_location', 'pickup_location']:
                seen_location, pickup_location = check_location(item_post_info)
                item_post.seen_location_id = seen_location.id if seen_location else item_post.seen_location_id
                item_post.pickup_location_id = pickup_location.id if pickup_location else item_post.pickup_location_id
            else:
                setattr(item_post, field, value)
        db.session.commit()
        return ItemPostSchema().dump(item_post), 201
    else:
        return {'error': 'Item post not found'}, 404


# Delete an item post
@item_posts_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_item_post(id):
    # Select item post matching id param from URL query
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
item_posts_bp.register_blueprint(locations_bp)
