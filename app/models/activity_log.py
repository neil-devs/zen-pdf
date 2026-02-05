from datetime import datetime
from app.extensions import db

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Nullable for anonymous users
    
    action = db.Column(db.String(64), nullable=False)   # e.g., 'LOGIN', 'MERGE_PDF', 'ERROR'
    ip_address = db.Column(db.String(45))               # IPv4 or IPv6
    details = db.Column(db.Text)                        # JSON string or description
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Log {self.action} by {self.user_id}>'