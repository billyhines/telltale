from app import db
from datetime import datetime


class SailingSession(db.Model):
    """Model for storing sailing session data and analytics."""
    __tablename__ = 'sailing_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    date = db.Column(db.Date, index=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer)  # Duration in seconds
    distance = db.Column(db.Float)  # Distance in nautical miles
    max_speed = db.Column(db.Float)  # Max speed in knots
    avg_speed = db.Column(db.Float)  # Average speed in knots
    location = db.Column(db.String(128))
    weather_conditions = db.Column(db.String(256))
    wind_speed = db.Column(db.Float)  # Wind speed in knots
    wind_direction = db.Column(db.String(16))  # N, NE, E, SE, etc.
    notes = db.Column(db.Text)
    gpx_file = db.Column(db.String(256))  # Path to uploaded GPX file
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    boat_id = db.Column(db.Integer, db.ForeignKey('boats.id'))
    
    # Performance metrics
    tacking_count = db.Column(db.Integer)  # Number of tacks
    jibing_count = db.Column(db.Integer)  # Number of jibes
    upwind_performance = db.Column(db.Float)  # Upwind performance metric
    downwind_performance = db.Column(db.Float)  # Downwind performance metric
    
    def __repr__(self):
        return f'<SailingSession {self.name} on {self.date}>'
    
    @property
    def formatted_duration(self):
        """Return formatted duration as HH:MM:SS."""
        if self.duration:
            hours, remainder = divmod(self.duration, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return "00:00:00"