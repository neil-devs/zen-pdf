from flask import Blueprint

# Define the blueprint object
core_bp = Blueprint('core', __name__)

# Import routes to register them with the blueprint
from app.blueprints.core import routes