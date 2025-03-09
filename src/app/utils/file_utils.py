import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
import gpxpy

def validate_gpx_file(file_storage):
    """
    Validate that the uploaded file is a valid GPX file
    
    Args:
        file_storage: FileStorage object from Flask
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Check if the file is present
    if not file_storage or file_storage.filename == '':
        return False, "No file selected"
    
    # Check the file extension
    if not file_storage.filename.lower().endswith('.gpx'):
        return False, "File must be a GPX file"
    
    # Try to parse the GPX data to validate its format
    try:
        content = file_storage.read()
        file_storage.seek(0)  # Reset file pointer after reading
        gpx = gpxpy.parse(content.decode('utf-8'))
        
        # Check if there are any tracks
        if not gpx.tracks:
            return False, "No track data found in GPX file"
        
        # Check if there are any points
        has_points = False
        for track in gpx.tracks:
            for segment in track.segments:
                if segment.points:
                    has_points = True
                    break
            if has_points:
                break
        
        if not has_points:
            return False, "No track points found in GPX file"
        
        return True, ""
        
    except Exception as e:
        return False, f"Invalid GPX file: {str(e)}"

def save_gpx_file(file_storage, user_id):
    """
    Save an uploaded GPX file to a secure location with a unique filename
    
    Args:
        file_storage: FileStorage object from Flask
        user_id: ID of the user who uploaded the file
        
    Returns:
        tuple: (success, file_path or error_message)
    """
    # Validate the file
    is_valid, error_message = validate_gpx_file(file_storage)
    if not is_valid:
        return False, error_message
    
    # Create upload directory if it doesn't exist
    upload_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads', str(user_id)))
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate a unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    original_filename = secure_filename(file_storage.filename)
    filename_base, filename_ext = os.path.splitext(original_filename)
    unique_filename = f"{filename_base}_{timestamp}_{str(uuid.uuid4())[:8]}{filename_ext}"
    file_path = os.path.join(str(user_id), unique_filename)
    full_path = os.path.join(upload_dir, unique_filename)
    
    # Save the file
    try:
        file_storage.save(full_path)
        return True, file_path
    except Exception as e:
        return False, f"Error saving file: {str(e)}"