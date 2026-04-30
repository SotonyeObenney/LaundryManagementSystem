from flask import Flask
from .extensions import db, login_manager, bcrypt, migrate
from config import Config
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

load_dotenv()

def create_app():
    app = Flask(__name__)    
    # Configuration
    app.config.from_object(Config)
    
    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return db.session.get(User, user_id)

    # 4. REGISTER BLUEPRINTS
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app