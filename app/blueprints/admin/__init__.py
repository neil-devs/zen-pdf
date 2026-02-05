from flask import Blueprint

# 1. Define the Blueprint
admin_bp = Blueprint('admin', __name__, template_folder='templates')

# 2. Import routes (Must be at bottom to avoid circular import)
from app.blueprints.admin import routes