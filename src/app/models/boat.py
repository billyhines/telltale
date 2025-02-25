from app import db
from datetime import datetime


class Boat(db.Model):
    """Boat model for storing boat-related data."""
    __tablename__ = 'boats'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    boat_type = db.Column(db.String(64))
    length = db.Column(db.Float)  # Length in meters
    manufacturer = db.Column(db.String(64))
    model = db.Column(db.String(64))
    year_built = db.Column(db.Integer)
    sail_number = db.Column(db.String(32))
    hull_id = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    sailing_sessions = db.relationship('SailingSession', backref='boat', lazy='dynamic')
    
    def __repr__(self):
        return f'<Boat {self.name}>'