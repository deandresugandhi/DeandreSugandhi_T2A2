"""
A module that defines the blueprint for routes involving records in the 
"comments" table.
"""


# Third-party Library Modules
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

# Local Modules
from setup import db
from models.comment import CommentSchema, Comment
from models.item_post import ItemPostSchema, ItemPost
from auth import authorize
from utilities import attach_image, clear_attached_images


comments_bp = Blueprint('comments', __name__, url_prefix='/<int:item_post_id>/comments')


# View comments on an item post
@comments_bp.route('/', methods=['GET'])
def view_comments(item_post_id):
    # Selects an item post from the db that matches the id
    stmt = db.select(ItemPost).filter_by(id=item_post_id)
    item_post = db.session.scalar(stmt)
    # Returns the item post, or error if the item post is not found
    if item_post:
        return ItemPostSchema(only=["comments"]).dump(item_post), 200
    return {'error': 'Item post not found'}, 404


# Create a comment
@comments_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment(item_post_id):
    # Parses incoming POST request body through CommentSchema
    comment_info = CommentSchema(only=['comment_text', 'images']).load(request.json)
    comment = Comment(
        comment_text = comment_info['comment_text'],
        user_id = get_jwt_identity(),
        item_post_id = item_post_id
    )
    db.session.add(comment)
    db.session.commit()

    # Create attached image records and associate them with the created comment
    attach_image(comment_info, comment, "comment")

    return CommentSchema().dump(comment), 201


# Edit a comment
@comments_bp.route('/<int:comment_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment(item_post_id, comment_id):
    # Parses incoming POST request body through ItemPostSchema
    comment_info = CommentSchema(only=['comment_text', 'images']).load(request.json)
    # Select comment matching id params from URL query
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    if comment:
        authorize(comment.user_id)
        # Change comment text
        comment.comment_text = comment_info.get('comment_text', comment.comment_text)
        # Change attached images by clearing all existing images and reattaching
        # new ones based on JSON from HTTP request, if images field exist in request
        if comment_info.get('images', ''):
            clear_attached_images(comment, "comment")
            attach_image(comment_info, comment, "comment")
        db.session.commit()
        return CommentSchema().dump(comment), 201
    else:
        return {'error': 'Comment not found'}, 404



# Delete a comment
@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(item_post_id, comment_id):
    # Select comment matching id params from URL query
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    if comment:
        authorize(comment.user_id)
        db.session.delete(comment)
        db.session.commit()
        return {}, 200
    else:
        return {'error': 'Comment not found'}, 404
    