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
    
    @classmethod
    def create_from_form(cls, form, user_id, gpx_file_path):
        """
        Create a new race instance from form data
        
        Args:
            form: The validated form data
            user_id: ID of the user who owns this race
            gpx_file_path: Path to the saved GPX file
            
        Returns:
            Race: The newly created Race instance
        """
        race = cls(
            user_id=user_id,
            race_name=form.race_name.data,
            race_date=form.race_date.data,
            gpx_file_path=gpx_file_path,
            is_processed=False
        )
        db.session.add(race)
        db.session.commit()
        return race
    
    def delete_with_data(self):
        """
        Delete this race and all associated data
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Delete the GPX file
            self.delete_gpx_file()
            
            # The relationships with cascade='all, delete-orphan' will 
            # handle deletion of related records automatically
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting race: {str(e)}")
            return False
    
    def to_dict(self):
        """
        Convert race to dictionary for API responses
        
        Returns:
            dict: Race data
        """
        return {
            'race_id': self.race_id,
            'user_id': self.user_id,
            'race_name': self.race_name,
            'race_date': self.race_date.isoformat() if self.race_date else None,
            'wind_direction': self.wind_direction,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_processed': self.is_processed,
            'total_distance': self.total_distance,
            'duration': self.duration,
            'duration_formatted': self.duration_formatted,
            'max_speed': self.max_speed,
            'avg_speed': self.avg_speed,
            'track_point_count': self.track_points.count() if self.track_points else 0,
            'mark_count': self.marks.count() if self.marks else 0
        }