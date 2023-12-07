from src.setup import db, ma
from marshmallow import fields

class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String, nullable=False)
    item_post_id = db.Column(db.Integer, db.ForeignKey('item_posts.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('images.id'))

class ImageSchema(ma.Schema):
    item_post = fields.Nested('ItemPostSchema', only=['id', 'title'])
    comment = fields.Nested('CommentSchema', only=['id', 'title'])

    class Meta:
        fields = ("id", "image_url", "item_post", "comment")
