from app import db
import enum
from datetime import datetime


class SegmentType(enum.Enum):
    """Enum for race segment types."""
    UPWIND = 'upwind'
    DOWNWIND = 'downwind'
    REACHING = 'reaching'


class RaceSegment(db.Model):
    """Model for storing race segment data."""
    __tablename__ = 'race_segments'
    
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('races.id'), index=True)
    segment_type = db.Column(db.Enum(SegmentType), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=True)  # Duration in seconds
    distance = db.Column(db.Float, nullable=True)  # Distance in nautical miles
    avg_speed = db.Column(db.Float, nullable=True)  # Average speed in knots
    max_speed = db.Column(db.Float, nullable=True)  # Maximum speed in knots
    vmg = db.Column(db.Float, nullable=True)  # Velocity Made Good
    start_mark_id = db.Column(db.Integer, db.ForeignKey('race_marks.id'), nullable=True)
    end_mark_id = db.Column(db.Integer, db.ForeignKey('race_marks.id'), nullable=True)
    leg_number = db.Column(db.Integer, nullable=True)  # Numerical order of the segment in the race
    
    # Relationships
    start_mark = db.relationship('RaceMark', foreign_keys=[start_mark_id], backref='segments_starting')
    end_mark = db.relationship('RaceMark', foreign_keys=[end_mark_id], backref='segments_ending')
    
    def __init__(self, **kwargs):
        super(RaceSegment, self).__init__(**kwargs)
        if self.start_time and self.end_time and not self.duration:
            self.duration = int((self.end_time - self.start_time).total_seconds())
    
    def calculate_statistics(self, track_points=None):
        """Calculate segment statistics from track points."""
        if not track_points:
            from app.models.track_point import TrackPoint
            track_points = TrackPoint.query.filter(
                TrackPoint.race_id == self.race_id,
                TrackPoint.timestamp >= self.start_time,
                TrackPoint.timestamp <= self.end_time
            ).order_by(TrackPoint.timestamp).all()
        
        if not track_points or len(track_points) < 2:
            return False
        
        # Calculate duration
        self.duration = int((self.end_time - self.start_time).total_seconds())
        
        # Calculate speeds
        speeds = [p.speed for p in track_points if p.speed is not None]
        if speeds:
            self.max_speed = max(speeds)
            self.avg_speed = sum(speeds) / len(speeds)
        
        # Calculate distance
        distances = [p.distance_to_next for p in track_points[:-1] if p.distance_to_next is not None]
        self.distance = sum(distances)
        
        # Calculate VMG if it's upwind or downwind
        if self.segment_type in (SegmentType.UPWIND, SegmentType.DOWNWIND):
            # This is a simplified calculation - in a real application, 
            # you'd need to consider the wind direction and boat heading
            vmg_values = [p.vmg for p in track_points if p.vmg is not None]
            if vmg_values:
                self.vmg = sum(vmg_values) / len(vmg_values)
        
        db.session.commit()
        return True
    
    @property
    def formatted_duration(self):
        """Return formatted duration as HH:MM:SS."""
        if self.duration:
            hours, remainder = divmod(self.duration, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return "00:00:00"
    
    def __repr__(self):
        return f'<RaceSegment {self.segment_type.value} from {self.start_time} to {self.end_time}>'