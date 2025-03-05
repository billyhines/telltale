from datetime import datetime
import enum
from app import db

class MarkType(enum.Enum):
    """Enum for race mark types"""
    START = 'start'
    FINISH = 'finish'
    WINDWARD = 'windward'
    LEEWARD = 'leeward'
    OFFSET = 'offset'
    OTHER = 'other'


class RaceMark(db.Model):
    """Model for race course marks"""
    __tablename__ = 'race_marks'
    
    mark_id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('races.race_id'), index=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    mark_type = db.Column(db.Enum(MarkType), nullable=False)
    name = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(RaceMark, self).__init__(**kwargs)
    
    @classmethod
    def get_marks_by_race(cls, race_id):
        """Get all marks for a specific race"""
        return cls.query.filter_by(race_id=race_id).all()
    
    @classmethod
    def get_mark_by_type(cls, race_id, mark_type):
        """Get a mark of a specific type for a race"""
        return cls.query.filter_by(race_id=race_id, mark_type=mark_type).first()
    
    @classmethod
    def create_or_update(cls, race_id, latitude, longitude, mark_type, name=None):
        """Create a new mark or update if exists for the given type"""
        existing = cls.query.filter_by(race_id=race_id, mark_type=mark_type).first()
        
        if existing:
            existing.latitude = latitude
            existing.longitude = longitude
            if name:
                existing.name = name
            existing.updated_at = datetime.utcnow()
            db.session.commit()
            return existing
        
        new_mark = cls(
            race_id=race_id,
            latitude=latitude,
            longitude=longitude,
            mark_type=mark_type,
            name=name
        )
        db.session.add(new_mark)
        db.session.commit()
        return new_mark
    
    def to_dict(self):
        """Convert mark to dictionary for API responses"""
        return {
            'mark_id': self.mark_id,
            'race_id': self.race_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'mark_type': self.mark_type.value,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<RaceMark {self.mark_type.value} ({self.latitude:.4f}, {self.longitude:.4f})>'