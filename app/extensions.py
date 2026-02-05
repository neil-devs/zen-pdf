from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from celery import Celery

# Initialize extensions (unbound to app)
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
csrf = CSRFProtect()
# --- ADD THIS LINE HERE ---
celery = Celery()
# Login Manager Setup
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # Blueprint.route
login_manager.login_message_category = 'info'