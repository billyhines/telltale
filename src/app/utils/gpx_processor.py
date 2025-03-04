import json
import math
import gpxpy
import gpxpy.gpx
from datetime import datetime

def process_gpx_file(gpx_file, user_id, session_name):
    """
    Process a GPX file and extract sailing data
    
    Args:
        gpx_file: The uploaded GPX file
        user_id: ID of the user who uploaded the file
        session_name: Name for the sailing session
        
    Returns:
        dict: Processed sailing data including points, stats, etc.
    """
    # Read GPX file content
    gpx_content = gpx_file.read().decode('utf-8')
    gpx_file.close()
    
    # Parse GPX data
    gpx = gpxpy.parse(gpx_content)
    
    # Initialize variables for calculations
    points = []
    speeds = []
    total_distance = 0
    prev_point = None
    
    # Get the track's start time
    start_time = None
    if gpx.tracks and gpx.tracks[0].segments and gpx.tracks[0].segments[0].points:
        start_time = gpx.tracks[0].segments[0].points[0].time
    
    # Process all track points
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                # Skip points without timestamp
                if not point.time:
                    continue
                
                # Calculate speed between points
                speed = 0
                if prev_point:
                    # Calculate distance in meters
                    distance = haversine(
                        prev_point.latitude, prev_point.longitude,
                        point.latitude, point.longitude
                    )
                    
                    # Calculate time difference in seconds
                    time_diff = (point.time - prev_point.time).total_seconds()
                    
                    if time_diff > 0:
                        # Speed in m/s, convert to knots (1 m/s = 1.94384 knots)
                        speed = (distance / time_diff) * 1.94384
                        total_distance += distance
                        speeds.append(speed)
                
                # Create point data for JSON storage
                point_data = {
                    'lat': point.latitude,
                    'lon': point.longitude,
                    'ele': point.elevation,
                    'time': point.time.isoformat(),
                    'speed': speed
                }
                points.append(point_data)
                prev_point = point
    
    # Calculate session statistics
    end_time = points[-1]['time'] if points else None
    duration = 0
    
    if start_time and end_time:
        start_time_dt = start_time
        end_time_dt = datetime.fromisoformat(end_time)
        duration = (end_time_dt - start_time_dt).total_seconds()
    
    # Convert total_distance from meters to kilometers
    total_distance = total_distance / 1000
    
    # Calculate max and average speed
    max_speed = max(speeds) if speeds else 0
    avg_speed = sum(speeds) / len(speeds) if speeds else 0
    
    # Prepare result data
    result = {
        'date': start_time,
        'duration': duration,
        'distance': total_distance,
        'max_speed': max_speed,
        'avg_speed': avg_speed,
        'points_json': json.dumps(points)
    }
    
    return result


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    
    Returns:
        float: Distance in meters
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371000  # Radius of earth in meters
    
    return c * r