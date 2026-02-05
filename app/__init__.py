from flask import Flask
from config import config_dict
from app.extensions import db, migrate, login_manager, bcrypt, csrf

def create_app(config_key='default'):
    """
    Application Factory Pattern.
    Creates and configures the Flask application.
    """
    app = Flask(__name__)
    
    # 1. Load Configuration
    app.config.from_object(config_dict[config_key])
    
    # --- ADD THIS BLOCK ---
    from app.extensions import celery
    celery.conf.update(app.config)

    # 2. Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    
    # 3. Register Blueprints (Modules)
    from app.blueprints.api.v1.endpoints import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    # We will register the 'Core' blueprint now to test the server.
    # We will uncomment the others as we build them.
    
    from app.blueprints.core import core_bp
    app.register_blueprint(core_bp)
    
    from app.blueprints.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.blueprints.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.blueprints.pdf_engine import pdf_bp
    app.register_blueprint(pdf_bp, url_prefix='/pdf')
    
    return app