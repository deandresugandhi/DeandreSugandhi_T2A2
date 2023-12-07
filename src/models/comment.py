from setup import db, ma
from datetime import datetime
from marshmallow import fields

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.Text, nullable=False)
    time_stamp = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_post_id = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False)


class CommentSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['id', 'username'])
    item_post = fields.Nested('ItemPostSchema', only=['id', 'title'])

    class Meta:
        fields = ("id", "comment_text", "time_stamp", "user", "item_post")
