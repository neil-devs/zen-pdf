import uuid
from datetime import datetime
from app.extensions import db

class FileMeta(db.Model):
    __tablename__ = 'file_meta'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Original name uploaded by user
    original_filename = db.Column(db.String(255), nullable=False)
    
    # Secure name stored on server
    stored_filename = db.Column(db.String(255), nullable=False)
    
    file_size = db.Column(db.Integer) # In bytes
    mime_type = db.Column(db.String(100))
    
    # Processing status: 'uploaded', 'processing', 'completed', 'failed'
    status = db.Column(db.String(20), default='uploaded')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime) # For auto-deletion policy

    def __repr__(self):
        return f'<File {self.original_filename} [{self.status}]>'