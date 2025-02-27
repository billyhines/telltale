from app import db
from datetime import datetime
import os


class Race(db.Model):
    """Model for storing race data and analytics."""
    __tablename__ = 'races'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    boat_id = db.Column(db.Integer, db.ForeignKey('boats.id'), index=True)
    race_name = db.Column(db.String(128), nullable=False)
    race_date = db.Column(db.Date, index=True, nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    duration = db.Column(db.Integer, nullable=True)  # Duration in seconds
    distance = db.Column(db.Float, nullable=True)  # Distance in nautical miles
    max_speed = db.Column(db.Float, nullable=True)  # Max speed in knots
    avg_speed = db.Column(db.Float, nullable=True)  # Average speed in knots
    location = db.Column(db.String(128), nullable=True)
    weather_conditions = db.Column(db.String(256), nullable=True)
    wind_speed = db.Column(db.Float, nullable=True)  # Wind speed in knots
    wind_direction = db.Column(db.String(16), nullable=True)  # N, NE, E, SE, etc.
    notes = db.Column(db.Text, nullable=True)
    gpx_file_path = db.Column(db.String(256), nullable=True)  # Path to uploaded GPX file
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    marks = db.relationship('RaceMark', backref='race', lazy='dynamic', cascade='all, delete-orphan')
    segments = db.relationship('RaceSegment', backref='race', lazy='dynamic', cascade='all, delete-orphan')
    maneuvers = db.relationship('Maneuver', backref='race', lazy='dynamic', cascade='all, delete-orphan')
    track_points = db.relationship('TrackPoint', backref='race', lazy='dynamic', cascade='all, delete-orphan')
    boat = db.relationship('Boat', backref='races')
    
    @property
    def formatted_duration(self):
        """Return formatted duration as HH:MM:SS."""
        if self.duration:
            hours, remainder = divmod(self.duration, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return "00:00:00"
    
    def delete_gpx_file(self):
        """Delete the associated GPX file if it exists."""
        if self.gpx_file_path and os.path.exists(self.gpx_file_path):
            try:
                os.remove(self.gpx_file_path)
                return True
            except Exception as e:
                # Log the error
                print(f"Error deleting GPX file: {str(e)}")
                return False
        return False
    
    def calculate_statistics(self):
        """Calculate race statistics from track points."""
        track_points = self.track_points.order_by(TrackPoint.timestamp).all()
        if not track_points or len(track_points) < 2:
            return False
            
        # Set start and end times from track points
        self.start_time = track_points[0].timestamp
        self.end_time = track_points[-1].timestamp
        
        # Calculate duration
        if self.start_time and self.end_time:
            self.duration = int((self.end_time - self.start_time).total_seconds())
        
        # Calculate speeds
        speeds = [p.speed for p in track_points if p.speed is not None]
        if speeds:
            self.max_speed = max(speeds)
            self.avg_speed = sum(speeds) / len(speeds)
        
        # Calculate distance
        # This is a simplified approach - for more accuracy, use haversine formula
        # between each consecutive point
        self.distance = sum(p.distance_to_next for p in track_points if p.distance_to_next is not None)
        
        db.session.commit()
        return True
    
    def __repr__(self):
        return f'<Race {self.race_name} on {self.race_date}>'