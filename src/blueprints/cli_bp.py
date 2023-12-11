"""
A module that defines the blueprint for terminal commands modifying the SQL
database.
"""


# Standard Library Modules
from datetime import date, datetime

# Third-party Library Modules
from flask import Blueprint

# Local Modules
from setup import db, bcrypt
from models.user import User
from models.item_post import ItemPost
from models.comment import Comment
from models.image import Image
from models.location import Location


db_commands = Blueprint('db', __name__)

@db_commands.cli.command("create")
def db_create():
    db.drop_all()
    db.create_all()
    print("Tables created")


@db_commands.cli.command("seed")
def db_seed():

   # Locations
    locations = [
        Location(
            street_number = 2,
            street_name = "Muller Lane",
            suburb = "Mascot",
            postcode = 2020,
            country = "Australia"
        ),
        Location(
            street_number = 1,
            street_name = "Kensington Road",
            suburb = "Kensington",
            postcode = 2033,
            country = "Australia"
        ),
    ]

    db.session.add_all(locations)
    db.session.commit()

    # Users
    users = [
        User(
            name="admin",
            username = "admin",
            email="admin@spam.com",
            password=bcrypt.generate_password_hash("admin").decode("utf8"),
            is_admin=True,
        ),
        User(
            name="John Doe",
            username="johndoe",
            email="johndoe@spam.com",
            password=bcrypt.generate_password_hash("johndoe").decode("utf8"),
        ),
        User(
            name="Jane Doe",
            username="janedoe",
            email="janedoe@spam.com",
            password=bcrypt.generate_password_hash("janedoe").decode("utf8"),
        ),
    ]

    db.session.add_all(users)
    db.session.commit()

    # Item Posts
    item_posts = [
        ItemPost(
            title="HP Laptop",
            item_type = "looking",
            category = "electronics",
            item_description = "Black HP laptop, with stickers",
            retrieval_description = "Please call 0451 123 456 if found",
            seen_location_id = locations[0].id,
            pickup_location_id = locations[1].id,
            status="unclaimed",
            date = date.today(),
            user_id = users[1].id
        ),
        ItemPost(
            title="Black UNIQLO T-Shirt",
            item_type = "found",
            category = "apparel",
            item_description="Black t-shirt, with blue decorations",
            retrieval_description = "Please call me on 0451 123 456 if it is yours",
            status="unclaimed",
            date=date.today(),
            user_id = users[1].id
        ),
        ItemPost(
            title="Black Kingston USB Device",
            item_type = "looking",
            category = "Electronics",
            item_description="Black Kingston USB with red decorations",
            retrieval_description = "Please call 0451 234 567 if found",
            status="pending",
            date=date.today(),
            user_id = users[2].id
        ),
    ]

    db.session.add_all(item_posts)
    db.session.commit()

    comments = [
        Comment(
            comment_text = "I think I may have found it, is this it? Check the photo",
            time_stamp = datetime.now(),
            user_id=users[2].id,
            item_post_id = item_posts[0].id
        ),
        Comment(
            comment_text = "That's the one, thanks! Where are you located?",
            time_stamp = datetime.now(),
            user_id=users[1].id,
            item_post_id = item_posts[0].id
        ),
        Comment(
            comment_text = "Comment 1",
            time_stamp = datetime.now(),
            user_id=users[1].id,
            item_post_id = item_posts[0].id
        )
    ]

    db.session.add_all(comments)
    db.session.commit()

    images = [
        Image(
            image_url = "image1.png",
            item_post_id = item_posts[0].id,
        ),
        Image(
            image_url = "image2.png",
            item_post_id = item_posts[1].id,
        ),
        Image(
            image_url = "image3.png",
            item_post_id = item_posts[2].id,
        ),
        Image(
            image_url = "image4.png",
            comment_id = comments[0].id,
        ),
    ]

    db.session.add_all(images)
    db.session.commit()

    print("Database seeded")
