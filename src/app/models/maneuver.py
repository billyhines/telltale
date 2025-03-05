from datetime import datetime
import enum
from app import db

class ManeuverType(enum.Enum):
    """Enum for maneuver types"""
    TACK = 'tack'
    GYBE = 'gybe'


class Maneuver(db.Model):
    """Model for sailing maneuvers analysis"""
    __tablename__ = 'maneuvers'
    
    maneuver_id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('races.race_id'), index=True)
    maneuver_type = db.Column(db.Enum(ManeuverType), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, index=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Performance metrics
    speed_before = db.Column(db.Float)  # Speed before maneuver in knots
    speed_after = db.Column(db.Float)   # Speed after maneuver in knots
    speed_loss = db.Column(db.Float)    # Speed loss during maneuver
    duration = db.Column(db.Float)      # Duration in seconds
    
    # Additional metrics
    entry_heading = db.Column(db.Float)  # Heading before maneuver
    exit_heading = db.Column(db.Float)   # Heading after maneuver
    heading_change = db.Column(db.Float) # Total heading change
    vmg_before = db.Column(db.Float)     # VMG before maneuver
    vmg_after = db.Column(db.Float)      # VMG after maneuver
    efficiency = db.Column(db.Float)     # Efficiency rating (0-100%)
    
    # Track point references
    start_point_id = db.Column(db.Integer, db.ForeignKey('track_points.point_id'))
    center_point_id = db.Column(db.Integer, db.ForeignKey('track_points.point_id'))
    end_point_id = db.Column(db.Integer, db.ForeignKey('track_points.point_id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    start_point = db.relationship('TrackPoint', foreign_keys=[start_point_id], backref='maneuver_starts')
    center_point = db.relationship('TrackPoint', foreign_keys=[center_point_id], backref='maneuver_centers')
    end_point = db.relationship('TrackPoint', foreign_keys=[end_point_id], backref='maneuver_ends')
    
    def __init__(self, **kwargs):
        super(Maneuver, self).__init__(**kwargs)
    
    @classmethod
    def get_maneuvers_by_race(cls, race_id):
        """Get all maneuvers for a specific race, ordered by timestamp"""
        return cls.query.filter_by(race_id=race_id).order_by(cls.timestamp).all()
    
    @classmethod
    def get_maneuvers_by_type(cls, race_id, maneuver_type):
        """Get maneuvers of a specific type for a race"""
        return cls.query.filter_by(
            race_id=race_id, 
            maneuver_type=maneuver_type
        ).order_by(cls.timestamp).all()
    
    @classmethod
    def get_best_maneuvers(cls, race_id, maneuver_type, limit=3):
        """Get the best maneuvers by efficiency"""
        return cls.query.filter_by(
            race_id=race_id,
            maneuver_type=maneuver_type
        ).order_by(cls.efficiency.desc()).limit(limit).all()
    
    @classmethod
    def get_worst_maneuvers(cls, race_id, maneuver_type, limit=3):
        """Get the worst maneuvers by efficiency"""
        return cls.query.filter_by(
            race_id=race_id,
            maneuver_type=maneuver_type
        ).order_by(cls.efficiency).limit(limit).all()
    
    @classmethod
    def get_maneuver_stats(cls, race_id):
        """Get aggregate statistics for maneuvers by type"""
        from sqlalchemy import func
        
        stats = {}
        for maneuver_type in ManeuverType:
            # Get aggregate data for this maneuver type
            result = db.session.query(
                func.count(cls.maneuver_id).label('count'),
                func.avg(cls.duration).label('avg_duration'),
                func.avg(cls.speed_loss).label('avg_speed_loss'),
                func.avg(cls.efficiency).label('avg_efficiency')
            ).filter_by(
                race_id=race_id,
                maneuver_type=maneuver_type
            ).first()
            
            if result and result.count:
                stats[maneuver_type.value] = {
                    'count': result.count,
                    'avg_duration': result.avg_duration,
                    'avg_speed_loss': result.avg_speed_loss,
                    'avg_efficiency': result.avg_efficiency
                }
        
        return stats
    
    def to_dict(self):
        """Convert maneuver to dictionary for API responses"""
        return {
            'maneuver_id': self.maneuver_id,
            'race_id': self.race_id,
            'maneuver_type': self.maneuver_type.value,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'speed_before': self.speed_before,
            'speed_after': self.speed_after,
            'speed_loss': self.speed_loss,
            'duration': self.duration,
            'entry_heading': self.entry_heading,
            'exit_heading': self.exit_heading,
            'heading_change': self.heading_change,
            'vmg_before': self.vmg_before,
            'vmg_after': self.vmg_after,
            'efficiency': self.efficiency
        }
    
    def __repr__(self):
        return f'<Maneuver {self.maneuver_type.value} at {self.timestamp}>'