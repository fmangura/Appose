from flask import Flask
from app.models import db, connect_db
import os

from config import Config

CURRENT_USER = 'curr_user_id'

def create_app():
    app = Flask(__name__)
    config_type = os.getenv('CONFIG_TYPE', default='config.Config')
    app.config.from_object(config_type)
    connect_db(app)
    app.app_context().push()

    # Initialize Flask extensions here
    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')

    from app.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    db.create_all()

    return app
