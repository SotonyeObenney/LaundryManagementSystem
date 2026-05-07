from flask import Flask
from .extensions import db, login_manager, bcrypt, migrate, mail
from config import Config
from dotenv import load_dotenv

load_dotenv

def create_app():
    app = Flask(__name__)    
    # Configuration
    app.config.from_object(Config)
    
    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return db.session.get(User, user_id)
    
    # Customize currency filter
    @app.template_filter('currency')
    def currency_filter(value):
        return "₦{:,.2f}".format(value)

    # 4. REGISTER BLUEPRINTS
    from app.auth import auth_bp
    from app.bookings import bookings_bp
    from app.staff import staff_bp
    from app.main import main_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(bookings_bp, url_prefix="/bookings")
    app.register_blueprint(staff_bp, url_prefix="/staff")
    app.register_blueprint(main_bp, url_prefix="/")

    return app