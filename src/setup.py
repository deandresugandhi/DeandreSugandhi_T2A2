from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from os import environ

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URI')

db = SQLAlchemy(app)
ma = Marshmallow(app)