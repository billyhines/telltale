from app import db
import enum
from datetime import datetime


class ManeuverType(enum.Enum):
    """Enum for maneuver types."""
    TACK = 'tack'
    GYBE = 'gybe'


class Maneuver(db.Model):
    """Model for storing sailing maneuvers data."""
    __tablename__ = 'maneuvers'
    
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('races.id'), index=True)
    maneuver_type = db.Column(db.Enum(ManeuverType), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, index=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    speed_before = db.Column(db.Float, nullable=True)  # Speed in knots before maneuver
    speed_after = db.Column(db.Float, nullable=True)   # Speed in knots after maneuver
    speed_loss = db.Column(db.Float, nullable=True)    # Speed loss during maneuver
    duration = db.Column(db.Integer, nullable=True)    # Duration in seconds
    heading_before = db.Column(db.Float, nullable=True)  # Heading in degrees before maneuver
    heading_after = db.Column(db.Float, nullable=True)   # Heading in degrees after maneuver
    heading_change = db.Column(db.Float, nullable=True)  # Change in heading in degrees
    quality_score = db.Column(db.Float, nullable=True)   # 0-100 score of maneuver quality
    segment_id = db.Column(db.Integer, db.ForeignKey('race_segments.id'), nullable=True)
    
    # Relationship
    segment = db.relationship('RaceSegment', backref='maneuvers')
    
    def calculate_statistics(self, track_points=None):
        """Calculate maneuver statistics from track points."""
        if not track_points:
            from app.models.track_point import TrackPoint
            
            # Get points before and after the maneuver for analysis
            # For a real application, you might need a more sophisticated approach
            # to determine exactly which track points to include
            buffer_seconds = 10  # Look 10 seconds before and after
            
            track_points = TrackPoint.query.filter(
                TrackPoint.race_id == self.race_id,
                TrackPoint.timestamp >= (self.timestamp - datetime.timedelta(seconds=buffer_seconds)),
                TrackPoint.timestamp <= (self.timestamp + datetime.timedelta(seconds=buffer_seconds))
            ).order_by(TrackPoint.timestamp).all()
        
        if not track_points or len(track_points) < 3:
            return False
        
        # Find the points closest to the maneuver timestamp
        closest_idx = 0
        min_delta = abs((track_points[0].timestamp - self.timestamp).total_seconds())
        
        for i, point in enumerate(track_points):
            delta = abs((point.timestamp - self.timestamp).total_seconds())
            if delta < min_delta:
                min_delta = delta
                closest_idx = i
        
        # Ensure we have points before and after
        if closest_idx == 0 or closest_idx == len(track_points) - 1:
            return False
        
        # Average speeds before and after
        before_points = track_points[:closest_idx]
        after_points = track_points[closest_idx+1:]
        
        if before_points and after_points:
            # Speed calculations
            self.speed_before = sum(p.speed for p in before_points if p.speed is not None) / len(before_points)
            self.speed_after = sum(p.speed for p in after_points if p.speed is not None) / len(after_points)
            self.speed_loss = max(0, self.speed_before - self.speed_after)
            
            # Heading calculations
            if all(p.heading is not None for p in before_points + after_points):
                self.heading_before = sum(p.heading for p in before_points) / len(before_points)
                self.heading_after = sum(p.heading for p in after_points) / len(after_points)
                
                # Calculate heading change (taking into account the 0-360 degree wrap)
                heading_change = self.heading_after - self.heading_before
                if heading_change > 180:
                    heading_change -= 360
                elif heading_change < -180:
                    heading_change += 360
                self.heading_change = abs(heading_change)
            
            # Duration calculation - find first and last points where a significant heading change occurs
            if self.heading_change and self.heading_change > 0:
                start_time = before_points[-1].timestamp
                end_time = after_points[0].timestamp
                self.duration = int((end_time - start_time).total_seconds())
                
                # Simple quality score based on speed loss and duration
                # A good maneuver minimizes speed loss and duration
                # This is a very simplified approach
                if self.speed_before > 0 and self.duration > 0:
                    speed_loss_ratio = self.speed_loss / self.speed_before
                    max_expected_duration = 20  # seconds
                    duration_ratio = min(1, self.duration / max_expected_duration)
                    
                    # Weighted combination (lower is better for both metrics)
                    combined_score = (0.7 * speed_loss_ratio) + (0.3 * duration_ratio)
                    
                    # Convert to 0-100 score (higher is better)
                    self.quality_score = 100 * (1 - combined_score)
        
        db.session.commit()
        return True
    
    def __repr__(self):
        return f'<Maneuver {self.maneuver_type.value} at {self.timestamp}>'