"""
A module that defines the blueprint for routes involving records in the 
"users" table.
"""


# Third-party Library Modules
from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

# Local Modules
from setup import db
from models.comment import CommentSchema, Comment
from auth import authorize


images_bp = Blueprint('comments', __name__, url_prefix='/<int:card_id>/comments')

# Create a comment
@comments_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment(item_post_id):
    comment_info = CommentSchema(only=['comment_text']).load(request.json)
    comment = Comment(
        comment_text = comment_info['comment_text'],
        user_id = get_jwt_identity(),
        item_post_id = item_post_id
    )
    db.session.add(comment)
    db.session.commit()
    return CommentSchema().dump(comment), 201

# Edit a comment
@comments_bp.route('/<int:comment_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment(item_post_id, comment_id):
    comment_info = CommentSchema(only=['message']).load(request.json)
    stmt = db.select(Comment).filter_by(id=comment_id) # .where(Comment.id == id)
    comment = db.session.scalar(stmt)
    if comment:
        authorize(comment.user_id)
        comment.message = comment_info.get('message', comment.message)
        db.session.commit()
        return CommentSchema().dump(comment)
    else:
        return {'error': 'Comment not found'}, 404

# Delete a comment
@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(item_post_id, comment_id):
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    if comment:
        authorize(comment.user_id)
        db.session.delete(comment)
        db.session.commit()
        return {}, 200
    else:
        return {'error': 'Comment not found'}, 404