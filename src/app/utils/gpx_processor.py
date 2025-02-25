import gpxpy
import gpxpy.gpx
import math
from datetime import datetime

def process_gpx_file(file_path):
    """
    Process a GPX file to extract relevant sailing data.
    
    Args:
        file_path: Path to the GPX file
        
    Returns:
        dict: Dictionary containing extracted data like distance, speeds, etc.
    """
    try:
        with open(file_path, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
            
            # Initialize variables
            total_distance = 0
            speeds = []
            start_time = None
            end_time = None
            points = []
            
            # Process tracks
            for track in gpx.tracks:
                for segment in track.segments:
                    prev_point = None
                    
                    for point in segment.points:
                        # Store point data
                        points.append(point)
                        
                        # Update start/end times
                        if start_time is None or point.time < start_time:
                            start_time = point.time
                        if end_time is None or point.time > end_time:
                            end_time = point.time
                        
                        # Calculate distance and speed
                        if prev_point:
                            # Distance between points in meters
                            distance = point.distance_3d(prev_point)
                            total_distance += distance
                            
                            # Speed in knots (1 m/s = 1.94384 knots)
                            if point.time and prev_point.time:
                                time_diff = (point.time - prev_point.time).total_seconds()
                                if time_diff > 0:
                                    speed_ms = distance / time_diff
                                    speed_knots = speed_ms * 1.94384
                                    speeds.append(speed_knots)
                        
                        prev_point = point
            
            # Calculate statistics
            avg_speed = sum(speeds) / len(speeds) if speeds else 0
            max_speed = max(speeds) if speeds else 0
            
            # Convert distance to nautical miles (1 meter = 0.000539957 nautical miles)
            distance_nm = total_distance * 0.000539957
            
            # Detect tacks and jibes (simplified algorithm)
            course_changes = []
            heading_changes = []
            
            if len(points) >= 3:
                for i in range(1, len(points) - 1):
                    if points[i-1].time and points[i+1].time:
                        # Calculate course before and after the point
                        course_before = calculate_bearing(points[i-1], points[i])
                        course_after = calculate_bearing(points[i], points[i+1])
                        
                        # Calculate absolute course change
                        course_change = abs(course_after - course_before)
                        if course_change > 180:
                            course_change = 360 - course_change
                        
                        course_changes.append(course_change)
            
            # Detect tacks (course changes between 80-120 degrees)
            tack_count = sum(1 for change in course_changes if 80 <= change <= 120)
            
            # Detect jibes (course changes between 140-180 degrees)
            jibe_count = sum(1 for change in course_changes if 140 <= change <= 180)
            
            return {
                'distance': round(distance_nm, 2),
                'max_speed': round(max_speed, 2),
                'avg_speed': round(avg_speed, 2),
                'start_time': start_time,
                'end_time': end_time,
                'tacking_count': tack_count,
                'jibing_count': jibe_count
            }
            
    except Exception as e:
        print(f"Error processing GPX file: {str(e)}")
        return None


def calculate_bearing(point1, point2):
    """
    Calculate the bearing (in degrees) between two GPS points.
    
    Args:
        point1: First GPX point
        point2: Second GPX point
        
    Returns:
        float: Bearing in degrees (0-360)
    """
    lat1 = math.radians(point1.latitude)
    lon1 = math.radians(point1.longitude)
    lat2 = math.radians(point2.latitude)
    lon2 = math.radians(point2.longitude)
    
    y = math.sin(lon2 - lon1) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)
    bearing = math.degrees(math.atan2(y, x))
    
    # Normalize to 0-360
    return (bearing + 360) % 360