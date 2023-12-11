"""
A module that defines the app's settings and how errors are handled globally.
"""


# Standard Library Modules
from os import environ

# Third-party Library Modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URI')

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.errorhandler(401)
def unauthorized(err):
    return {'error': 'You are not authorized to access this resource'}

@app.errorhandler(ValidationError)
def validation_error(err):
    return {'error': err.messages}

@app.errorhandler(IntegrityError)
def integrity_error(err):
    return {'error': err.messages}
