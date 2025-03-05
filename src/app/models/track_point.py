from datetime import datetime
from app import db

class TrackPoint(db.Model):
    """Model for storing individual GPS track points from GPX data"""
    __tablename__ = 'track_points'
    
    point_id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('races.race_id'), index=True)
    
    # Location data
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    elevation = db.Column(db.Float)  # In meters, nullable
    
    # Time data
    timestamp = db.Column(db.DateTime, nullable=False, index=True)
    
    # Calculated metrics
    speed = db.Column(db.Float)      # In knots
    heading = db.Column(db.Float)    # In degrees (0-360)
    vmg = db.Column(db.Float)        # Velocity Made Good (calculated later)
    
    # Wind angle data (calculated based on wind direction)
    true_wind_angle = db.Column(db.Float)  # Angle between boat heading and wind
    
    # Sequential tracking
    point_index = db.Column(db.Integer, index=True)  # Index in the sequence
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(TrackPoint, self).__init__(**kwargs)
    
    @classmethod
    def get_points_by_race(cls, race_id, limit=None, offset=None):
        """Get track points for a race, with optional pagination"""
        query = cls.query.filter_by(race_id=race_id).order_by(cls.timestamp)
        
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
            
        return query.all()
    
    @classmethod
    def get_point_count(cls, race_id):
        """Get total number of points for a race"""
        return cls.query.filter_by(race_id=race_id).count()
    
    @classmethod
    def get_points_in_timerange(cls, race_id, start_time, end_time):
        """Get points between start and end times"""
        return cls.query.filter(
            cls.race_id == race_id,
            cls.timestamp >= start_time,
            cls.timestamp <= end_time
        ).order_by(cls.timestamp).all()
    
    @classmethod
    def get_point_at_time(cls, race_id, timestamp):
        """Get the point closest to the given timestamp"""
        # First try exact match
        point = cls.query.filter_by(race_id=race_id, timestamp=timestamp).first()
        if point:
            return point
        
        # Otherwise get closest before and after
        before = cls.query.filter(
            cls.race_id == race_id,
            cls.timestamp <= timestamp
        ).order_by(cls.timestamp.desc()).first()
        
        after = cls.query.filter(
            cls.race_id == race_id,
            cls.timestamp >= timestamp
        ).order_by(cls.timestamp).first()
        
        # Return closest of the two
        if not before:
            return after
        if not after:
            return before
        
        before_diff = (timestamp - before.timestamp).total_seconds()
        after_diff = (after.timestamp - timestamp).total_seconds()
        
        return before if before_diff <= after_diff else after
    
    def calculate_vmg(self, wind_direction):
        """Calculate VMG based on current speed, heading and wind direction"""
        if self.speed is None or self.heading is None or wind_direction is None:
            return None
        
        import math
        # Calculate the true wind angle (angle between boat heading and wind)
        wind_angle = abs((self.heading - wind_direction + 180) % 360 - 180)
        
        # Calculate VMG using speed and the cosine of the angle
        vmg = self.speed * math.cos(math.radians(wind_angle))
        
        return vmg
    
    def to_dict(self):
        """Convert track point to dictionary for API responses"""
        return {
            'point_id': self.point_id,
            'race_id': self.race_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'elevation': self.elevation,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'speed': self.speed,
            'heading': self.heading,
            'vmg': self.vmg,
            'true_wind_angle': self.true_wind_angle,
            'point_index': self.point_index
        }
    
    def to_geojson(self):
        """Convert track point to GeoJSON format"""
        properties = {
            'point_id': self.point_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'speed': self.speed,
            'heading': self.heading,
            'vmg': self.vmg
        }
        
        return {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [self.longitude, self.latitude]
            },
            'properties': properties
        }
    
    def __repr__(self):
        return f'<TrackPoint {self.point_id} at {self.timestamp}>'