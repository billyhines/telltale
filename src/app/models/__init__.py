# Import all models for use in Flask shell context and migrations
from app.models.user import User
from app.models.race import Race
from app.models.race_mark import RaceMark
from app.models.race_segment import RaceSegment
from app.models.maneuver import Maneuver
from app.models.track_point import TrackPoint