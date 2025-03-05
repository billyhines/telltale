from datetime import datetime
import enum
from app import db

class SegmentType(enum.Enum):
    """Enum for race segment types"""
    UPWIND = 'upwind'
    DOWNWIND = 'downwind'
    REACHING = 'reaching'


class RaceSegment(db.Model):
    """Model for race segment analysis"""
    __tablename__ = 'race_segments'
    
    segment_id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('races.race_id'), index=True)
    segment_type = db.Column(db.Enum(SegmentType), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    avg_speed = db.Column(db.Float)  # In knots
    distance = db.Column(db.Float)   # In nautical miles
    avg_vmg = db.Column(db.Float)    # Average VMG for the segment
    start_index = db.Column(db.Integer)  # Index of starting track point
    end_index = db.Column(db.Integer)    # Index of ending track point
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(RaceSegment, self).__init__(**kwargs)
    
    @property
    def duration(self):
        """Calculate duration of segment in seconds"""
        if not self.start_time or not self.end_time:
            return 0
        return (self.end_time - self.start_time).total_seconds()
    
    @property
    def duration_formatted(self):
        """Format duration in HH:MM:SS"""
        duration_secs = self.duration
        hours, remainder = divmod(duration_secs, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    
    @classmethod
    def get_segments_by_race(cls, race_id):
        """Get all segments for a specific race, ordered by start time"""
        return cls.query.filter_by(race_id=race_id).order_by(cls.start_time).all()
    
    @classmethod
    def get_segments_by_type(cls, race_id, segment_type):
        """Get segments of a specific type for a race"""
        return cls.query.filter_by(
            race_id=race_id, 
            segment_type=segment_type
        ).order_by(cls.start_time).all()
    
    @classmethod
    def get_segment_stats_by_type(cls, race_id):
        """Get aggregate statistics for each segment type"""
        from sqlalchemy import func
        
        stats = {}
        for segment_type in SegmentType:
            # Get aggregate data for this segment type
            result = db.session.query(
                func.count(cls.segment_id).label('count'),
                func.sum(cls.distance).label('total_distance'),
                func.avg(cls.avg_speed).label('avg_speed'),
                func.avg(cls.avg_vmg).label('avg_vmg')
            ).filter_by(
                race_id=race_id,
                segment_type=segment_type
            ).first()
            
            if result and result.count:
                stats[segment_type.value] = {
                    'count': result.count,
                    'total_distance': result.total_distance,
                    'avg_speed': result.avg_speed,
                    'avg_vmg': result.avg_vmg
                }
        
        return stats
    
    def to_dict(self):
        """Convert segment to dictionary for API responses"""
        return {
            'segment_id': self.segment_id,
            'race_id': self.race_id,
            'segment_type': self.segment_type.value,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration': self.duration,
            'duration_formatted': self.duration_formatted,
            'avg_speed': self.avg_speed,
            'distance': self.distance,
            'avg_vmg': self.avg_vmg,
            'start_index': self.start_index,
            'end_index': self.end_index
        }
    
    def __repr__(self):
        return f'<RaceSegment {self.segment_type.value} {self.start_time} to {self.end_time}>'