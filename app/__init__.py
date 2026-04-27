from flask import Flask

from app.models.user import User
from .extensions import db, login_manager, bcrypt, migrate
from config import Config
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

#initializing the db and the db orm


def create_app():
    load_dotenv()
    app = Flask(__name__, template_folder='../templates')    
    #app.config.from_object(Config)
    # 1. CONFIGURATION FIRST
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///laundry.db'
    
    # 2. INITIALIZE EXTENSIONS
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 4. REGISTER BLUEPRINTS
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app