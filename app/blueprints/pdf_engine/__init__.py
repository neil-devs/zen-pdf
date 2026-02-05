from flask import Blueprint

pdf_bp = Blueprint('pdf_engine', __name__)

from app.blueprints.pdf_engine import routes