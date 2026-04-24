from flask import Flask
from .extensions import db, login_manager, bcrypt, migrate
from config import Config



def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(Config)

    # ADD THIS LINE temporarily
    print(f"DEBUG: Flask is looking for templates in: {app.template_folder}")

    # Initialize extensions
    db.init_app(app)
    # login_manager.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Register blueprints
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app