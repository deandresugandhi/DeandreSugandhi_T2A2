"""
A module that defines the main file from which the web app is run.
"""


# Local Modules
from setup import app
from blueprints.cli_bp import db_commands
from blueprints.item_posts_bp import item_posts_bp
from blueprints.users_bp import users_bp
from blueprints.comments_bp import comments_bp


app.register_blueprint(db_commands)
app.register_blueprint(item_posts_bp)
app.register_blueprint(users_bp)
app.register_blueprint(comments_bp)

# print(app.url_map)
