# Third-party Library Modules
from marshmallow import fields

# Local Modules
from setup import db, ma


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.Text, nullable=False)
    time_stamp = db.Column(db.DateTime, nullable=False)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_post_id = db.Column(db.Integer, db.ForeignKey('item_posts.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='comments')
    item_post = db.relationship('ItemPost', back_populates='comments')
    images = db.relationship('Image', back_populates='comment')

class CommentSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['id', 'username'])

    class Meta:
        fields = ("id", "comment_text", "time_stamp", "user")
