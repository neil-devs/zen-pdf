from flask import render_template
from app.blueprints.core import core_bp

# 1. NEW LANDING PAGE (Root URL)
@core_bp.route('/')
def landing():
    """
    The public welcome page with animations.
    """
    return render_template('core/landing.html', title="Welcome")

# 2. THE DASHBOARD (Moved to /dashboard)
@core_bp.route('/dashboard')
def dashboard():
    """
    The main tool interface (formerly the index page).
    """
    return render_template('core/index.html', title="Dashboard")

# 3. EDITOR ROUTE (Unchanged)
@core_bp.route('/tools/editor')
def pdf_editor():
    """
    Route to serve the PDF Canvas Editor.
    """
    return render_template('pdf/canvas_ui.html', title="Editor")