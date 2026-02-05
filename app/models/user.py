from datetime import datetime
from flask_login import UserMixin
from app.extensions import db, bcrypt, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Roles: 'user' or 'admin'
    role = db.Column(db.String(20), default='user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    logs = db.relationship('ActivityLog', backref='user', lazy=True)
    files = db.relationship('FileMeta', backref='owner', lazy=True)

    def set_password(self, password):
        """Hashes the password before storing."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Verifies password against hash."""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username}>'

# Helper for Flask-Login to reload user from session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))