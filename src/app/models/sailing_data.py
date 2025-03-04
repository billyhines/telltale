from datetime import datetime
import json
from app import db

class SailingSession(db.Model):
    """Model for storing sailing sessions data from GPX files"""
    __tablename__ = 'sailing_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    date = db.Column(db.DateTime, index=True)
    duration = db.Column(db.Integer)  # Duration in seconds
    distance = db.Column(db.Float)    # Distance in kilometers
    max_speed = db.Column(db.Float)   # Max speed in knots
    avg_speed = db.Column(db.Float)   # Average speed in knots
    points_json = db.Column(db.Text)  # JSON string of GPS points
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    
    def __init__(self, **kwargs):
        super(SailingSession, self).__init__(**kwargs)
    
    @property
    def points(self):
        """Deserialize points_json to Python object"""
        return json.loads(self.points_json) if self.points_json else []
    
    @property
    def duration_formatted(self):
        """Format duration in HH:MM:SS"""
        hours, remainder = divmod(self.duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    
    def __repr__(self):
        return f'<SailingSession {self.name} {self.date}>'


class SailingCondition(db.Model):
    """Model for storing weather/condition data for sailing sessions"""
    __tablename__ = 'sailing_conditions'
    
    id = db.Column(db.Integer, primary_key=True)
    wind_speed = db.Column(db.Float)          # Wind speed in knots
    wind_direction = db.Column(db.Integer)    # Wind direction in degrees
    wave_height = db.Column(db.Float)         # Wave height in meters
    temperature = db.Column(db.Float)         # Temperature in Celsius
    weather_notes = db.Column(db.Text)        # Any additional weather notes
    
    # Foreign key to SailingSession
    session_id = db.Column(db.Integer, db.ForeignKey('sailing_sessions.id'), index=True)
    session = db.relationship('SailingSession', backref=db.backref('conditions', uselist=False))
    
    def __repr__(self):
        return f'<SailingCondition {self.wind_speed}kt {self.wind_direction}°>'