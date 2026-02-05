import os
from app import create_app
from app.extensions import celery

# 1. Initialize the Flask Application
# We need the app context so the worker can access the Database and Config
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.app_context().push()

# 2. This file is the entry point for the "Background Worker"
# When you deploy to a real server, you run this file separately to process PDFs.