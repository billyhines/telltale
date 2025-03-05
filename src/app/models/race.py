from datetime import datetime
import os
from app import db

class Race(db.Model):
    """Model for storing sailing race data"""
    __tablename__ = 'races'
    
    race_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    race_name = db.Column(db.String(128), nullable=False)
    race_date = db.Column(db.DateTime, nullable=False, index=True)
    gpx_file_path = db.Column(db.String(256), nullable=False)
    wind_direction = db.Column(db.Integer)  # Direction in degrees
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Processing status flags
    is_processed = db.Column(db.Boolean, default=False)
    processing_error = db.Column(db.Text)
    
    # Race statistics
    total_distance = db.Column(db.Float)  # In nautical miles
    duration = db.Column(db.Integer)  # In seconds
    max_speed = db.Column(db.Float)  # In knots
    avg_speed = db.Column(db.Float)  # In knots
    
    # Relationships
    marks = db.relationship('RaceMark', backref='race', lazy='dynamic', cascade='all, delete-orphan')
    segments = db.relationship('RaceSegment', backref='race', lazy='dynamic', cascade='all, delete-orphan')
    maneuvers = db.relationship('Maneuver', backref='race', lazy='dynamic', cascade='all, delete-orphan')
    track_points = db.relationship('TrackPoint', backref='race', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        super(Race, self).__init__(**kwargs)
    
    @property
    def duration_formatted(self):
        """Format duration in HH:MM:SS"""
        if not self.duration:
            return "00:00:00"
        
        hours, remainder = divmod(self.duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    
    def get_gpx_full_path(self, base_dir=None):
        """Get full path to GPX file"""
        if not base_dir:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads'))
        return os.path.join(base_dir, self.gpx_file_path)
    
    def get_track_boundaries(self):
        """Get min/max lat/lon values for the track"""
        if not self.track_points.count():
            return None
        
        min_lat = db.session.query(db.func.min(TrackPoint.latitude)).filter_by(race_id=self.race_id).scalar()
        max_lat = db.session.query(db.func.max(TrackPoint.latitude)).filter_by(race_id=self.race_id).scalar()
        min_lon = db.session.query(db.func.min(TrackPoint.longitude)).filter_by(race_id=self.race_id).scalar()
        max_lon = db.session.query(db.func.max(TrackPoint.longitude)).filter_by(race_id=self.race_id).scalar()
        
        return {
            'min_lat': min_lat,
            'max_lat': max_lat,
            'min_lon': min_lon,
            'max_lon': max_lon
        }
    
    def get_time_range(self):
        """Get first and last timestamp of the track"""
        if not self.track_points.count():
            return None
        
        first_point = self.track_points.order_by(TrackPoint.timestamp).first()
        last_point = self.track_points.order_by(TrackPoint.timestamp.desc()).first()
        
        return {
            'start_time': first_point.timestamp,
            'end_time': last_point.timestamp
        }
    
    def get_speed_range(self):
        """Get min/max speed values"""
        if not self.track_points.count():
            return None
        
        min_speed = db.session.query(db.func.min(TrackPoint.speed)).filter_by(race_id=self.race_id).scalar() or 0
        max_speed = db.session.query(db.func.max(TrackPoint.speed)).filter_by(race_id=self.race_id).scalar() or 0
        
        return {
            'min_speed': min_speed,
            'max_speed': max_speed
        }
    
    def delete_gpx_file(self):
        """Delete GPX file from filesystem"""
        if self.gpx_file_path:
            try:
                full_path = self.get_gpx_full_path()
                if os.path.exists(full_path):
                    os.remove(full_path)
                    return True
            except Exception as e:
                # Log the error
                print(f"Error deleting GPX file: {str(e)}")
        return False
    
    def __repr__(self):
        return f'<Race {self.race_name} {self.race_date}>'