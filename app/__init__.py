from flask import Flask
from .extensions import db, migrate, login_manager
from .main import main_bp
from .auth import auth_bp
from .store import store_bp
from .dashboard import dashboard_bp
from .admin import admin_bp
from config import Config
import os


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Import models to ensure they are registered with SQLAlchemy
    from . import models
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(store_bp, url_prefix='/store')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Create database tables
    with app.app_context():
        try:
            # Ensure instance directory exists
            if not os.path.exists(app.instance_path):
                os.makedirs(app.instance_path)
            
            # Create database tables
            db.create_all()
            print("✓ Database initialized successfully")
        except Exception as e:
            print(f"⚠️ Database initialization warning: {e}")
            print("Database will be created when first accessed")
    
    return app
