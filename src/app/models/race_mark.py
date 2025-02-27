from app import db
import enum


class MarkType(enum.Enum):
    """Enum for race mark types."""
    START = 'start'
    FINISH = 'finish'
    WINDWARD = 'windward'
    LEEWARD = 'leeward'
    OFFSET = 'offset'
    OTHER = 'other'


class RaceMark(db.Model):
    """Model for storing race mark data."""
    __tablename__ = 'race_marks'
    
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('races.id'), index=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    mark_type = db.Column(db.Enum(MarkType), nullable=False)
    name = db.Column(db.String(64), nullable=True)
    description = db.Column(db.String(256), nullable=True)
    rounding_order = db.Column(db.Integer, nullable=True)  # Order in which marks are rounded
    
    def __repr__(self):
        return f'<RaceMark {self.mark_type.value} at ({self.latitude}, {self.longitude})>'
    
    def to_dict(self):
        """Convert mark to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'race_id': self.race_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'mark_type': self.mark_type.value,
            'name': self.name,
            'description': self.description,
            'rounding_order': self.rounding_order
        }
    
    @staticmethod
    def from_dict(data):
        """Create a RaceMark from dictionary data."""
        return RaceMark(
            race_id=data.get('race_id'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            mark_type=MarkType(data.get('mark_type')),
            name=data.get('name'),
            description=data.get('description'),
            rounding_order=data.get('rounding_order')
        )