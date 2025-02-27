from app import db
import math
from datetime import datetime


class TrackPoint(db.Model):
    """Model for storing GPS track points from GPX files."""
    __tablename__ = 'track_points'
    
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('races.id'), index=True)
    timestamp = db.Column(db.DateTime, nullable=False, index=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    elevation = db.Column(db.Float, nullable=True)  # Elevation in meters
    speed = db.Column(db.Float, nullable=True)      # Speed in knots
    heading = db.Column(db.Float, nullable=True)    # Heading in degrees (0-360)
    vmg = db.Column(db.Float, nullable=True)        # Velocity Made Good toward next mark
    distance_to_next = db.Column(db.Float, nullable=True)  # Distance to next point in nautical miles
    segment_id = db.Column(db.Integer, db.ForeignKey('race_segments.id'), nullable=True)
    
    # Relationship
    segment = db.relationship('RaceSegment', backref='track_points')
    
    def __repr__(self):
        return f'<TrackPoint {self.timestamp} at ({self.latitude}, {self.longitude})>'
    
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """
        Calculate the distance between two points in nautical miles using the haversine formula.
        """
        # Convert to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Haversine formula
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        # Radius of Earth in nautical miles
        radius = 3440.07  # 6371 km converted to nautical miles
        distance = radius * c
        
        return distance
    
    @staticmethod
    def calculate_heading(lat1, lon1, lat2, lon2):
        """
        Calculate the heading between two points in degrees (0-360).
        """
        # Convert to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Calculate heading
        dlon = lon2_rad - lon1_rad
        y = math.sin(dlon) * math.cos(lat2_rad)
        x = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon)
        heading_rad = math.atan2(y, x)
        
        # Convert to degrees and normalize to 0-360
        heading_deg = math.degrees(heading_rad)
        heading_deg = (heading_deg + 360) % 360
        
        return heading_deg
    
    @staticmethod
    def calculate_speed(distance, time_diff):
        """
        Calculate speed in knots given distance in nautical miles and time in seconds.
        """
        if time_diff <= 0:
            return None
        
        # Convert to hours
        time_hours = time_diff / 3600
        
        # Speed in knots
        speed = distance / time_hours
        
        return speed
    
    @staticmethod
    def calculate_vmg(speed, heading, wind_direction):
        """
        Calculate Velocity Made Good (VMG) given speed, heading, and wind direction.
        
        For upwind sailing, VMG is positive when sailing towards the wind.
        For downwind sailing, VMG is positive when sailing away from the wind.
        """
        if speed is None or heading is None or wind_direction is None:
            return None
        
        # Convert wind direction to degrees if it's a string like 'N', 'SW', etc.
        if isinstance(wind_direction, str):
            direction_map = {
                'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5,
                'E': 90, 'ESE': 112.5, 'SE': 135, 'SSE': 157.5,
                'S': 180, 'SSW': 202.5, 'SW': 225, 'WSW': 247.5,
                'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5
            }
            wind_direction = direction_map.get(wind_direction.upper(), None)
            if wind_direction is None:
                return None
        
        # Calculate the absolute angle between boat heading and wind direction
        angle = abs(heading - wind_direction)
        if angle > 180:
            angle = 360 - angle
        
        # Calculate VMG
        vmg = speed * math.cos(math.radians(angle))
        
        return vmg
    
    @classmethod
    def generate_from_gpx(cls, race_id, gpx_file_path, wind_direction=None):
        """
        Generate TrackPoint instances from a GPX file.
        
        Args:
            race_id: ID of the race
            gpx_file_path: Path to the GPX file
            wind_direction: Wind direction in degrees or as string ('N', 'SW', etc.)
            
        Returns:
            list: List of created TrackPoint instances
        """
        import gpxpy
        
        track_points = []
        
        try:
            with open(gpx_file_path, 'r') as gpx_file:
                gpx = gpxpy.parse(gpx_file)
                
                for track in gpx.tracks:
                    for segment in track.segments:
                        prev_point = None
                        
                        for point in segment.points:
                            track_point = cls(
                                race_id=race_id,
                                timestamp=point.time,
                                latitude=point.latitude,
                                longitude=point.longitude,
                                elevation=point.elevation,
                            )
                            
                            # Calculate speed, heading, and distance if we have a previous point
                            if prev_point:
                                # Calculate distance to this point from the previous one
                                distance = cls.calculate_distance(
                                    prev_point.latitude, prev_point.longitude,
                                    point.latitude, point.longitude
                                )
                                prev_point.distance_to_next = distance
                                
                                # Calculate time difference in seconds
                                time_diff = (point.time - prev_point.timestamp).total_seconds()
                                
                                # Calculate speed
                                if time_diff > 0:
                                    prev_point.speed = cls.calculate_speed(distance, time_diff)
                                
                                # Calculate heading
                                prev_point.heading = cls.calculate_heading(
                                    prev_point.latitude, prev_point.longitude,
                                    point.latitude, point.longitude
                                )
                                
                                # Calculate VMG
                                if prev_point.speed is not None and prev_point.heading is not None and wind_direction is not None:
                                    prev_point.vmg = cls.calculate_vmg(
                                        prev_point.speed, prev_point.heading, wind_direction
                                    )
                            
                            track_points.append(track_point)
                            prev_point = track_point
                            
                        # Handle the last point
                        if track_points and len(track_points) > 1:
                            last_point = track_points[-1]
                            # Last point doesn't have a next point, so set distance_to_next to 0
                            last_point.distance_to_next = 0
                            
                            # For the last point, we can use the same heading as the previous point
                            if len(track_points) > 1:
                                second_last_point = track_points[-2]
                                if second_last_point.heading is not None:
                                    last_point.heading = second_last_point.heading
                                
                                # For speed, we can use the same speed as the previous point
                                if second_last_point.speed is not None:
                                    last_point.speed = second_last_point.speed
                                    
                                    # Calculate VMG for the last point
                                    if last_point.heading is not None and wind_direction is not None:
                                        last_point.vmg = cls.calculate_vmg(
                                            last_point.speed, last_point.heading, wind_direction
                                        )
                
                # Add all track points to the database
                for point in track_points:
                    db.session.add(point)
                db.session.commit()
                    
                return track_points
                
        except Exception as e:
            # Log the error
            print(f"Error processing GPX file: {str(e)}")
            # Rollback any partial changes
            db.session.rollback()
            return []