# Third-party Library Modules
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError

# Local Modules
from setup import db
from models.location import Location, LocationSchema
from models.image import Image, ImageSchema


def check_location(parsed_info):
    """
    A function that checks for the locations in an item_post. If the location
    does not exist yet, the location is registered to the locations table in
    the db. Otherwise, the location is retrieved from the locations table in
    the db.

    Args:
    1. raw_info (dict): The raw_info is a dictionary parsed through a specific
    schema, with keys that contain a location dictionary.
    """
    def register_location(parsed_info, location_attribute):
        """
        Registers the location if it is not already registered into the db.

        Args:
        1. parsed_info (dict): A dictionary parsed through a specific
        schema, with keys that contain a location dictionary that follows the
        LocationSchema.
        2. location_attribute (str): The location attribute refers to either
        "seen_location" or "pickup_location" key of the raw_info dictionary.
        """
        if location_attribute not in parsed_info:
            return None
        location_data = parsed_info[location_attribute]
        location_info = LocationSchema().load(location_data)
        stmt = db.select(Location).filter_by(**location_info)
        existing_location = db.session.scalar(stmt)
        # If location exists already, returns existing location instead of
        # registering a new location
        if existing_location:
            return existing_location
        else:
            location = Location(**location_info)
            # Session added but not committed, for error handling purposes.
            db.session.add(location)
            return location

    try:
        seen_location = register_location(parsed_info, 'seen_location')
        pickup_location = register_location(parsed_info, 'pickup_location')
        db.session.commit()
    # IntegrityError is raised if unique combination constraint is violated
    # during commit, ValidationError is raised if the requirements in the
    # LocationSchema is violated, such as missing required fields
    except (ValidationError, IntegrityError) as err:
        db.session.rollback()
        return {'error': str(err)}, 404
    return seen_location, pickup_location


def attach_image(parsed_info, record, model):
    """
    A function for attaching an image into a record, namely comment and
    item post.

    Args:
    1. parsed_info (dict): A dictionary parsed through a specific schema, 
    with keys that contain image dictionaries.
    2. record (Model instance): The record which the image will be attached to.
    3. model (str): The name of the model in which to attach the image, i.e.
    "comment" or "item_post"
    """
    model_id = model + "_id"

    # Check if there are any images that need to be attached in the parsed information.
    if parsed_info.get("images", ""):
        for image in parsed_info.get("images"):
            image_info = ImageSchema(only=["image_url"]).load(image)
            if image_info:
                attached_image = Image(
                    image_url=image.get("image_url"),
                )
                # Set model_id (foreign key referring to comment / item post record)
                setattr(attached_image, model_id, record.id)
                db.session.add(attached_image)

    # Commit the new image records to the database only if all image are
    # successfully validated
    db.session.commit()


def clear_attached_images(record, model):
    model_id = model + "_id"
    stmt = db.select(Image).filter(getattr(Image, model_id) == record.id)
    attached_images = db.session.scalars(stmt).all()
    for image in attached_images:
        db.session.delete(image)
    db.session.commit()
