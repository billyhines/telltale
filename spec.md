# Sailing Analytics Platform Specification

## Overview

A web-based platform for casual weekend racers to analyze their sailing performance through uploaded tracks. The platform will provide multi-level analysis of sailing data, from basic track visualization to detailed maneuver analysis.

## User Experience

- Target users: Experienced sailors/racers
- Primary device: Desktop computers
- User authentication required
- Private data by default (sharing features to be added later)

## Core Features

### Level 1: Basic Track Visualization

- Display sailing track on a basic map using Leaflet
- Visualize speed using a dynamic blue-to-red color gradient on the track
- Include a time slider for race playback at adjustable speeds

### Level 2: Performance Analysis

- Wind direction input via visual compass selector with numerical display
- Manual race course mark plotting by clicking on track
- Calculate and display:
    - Velocity Made Good (VMG)
    - Headers and lifts
    - Time sailing upwind/downwind
    - Average speed upwind/downwind

### Level 3: Maneuver Analysis

- Detect tacks and gybes (direction changes >45 degrees)
- Calculate speed loss during maneuvers using trailing average speeds
- Visualize maneuvers by overlaying all tacks/gybes together
    - Show both aggregate averages (bold lines) and individual maneuvers (dotted lines)
    - Center visualization at the maneuver point (0 on time axis)
    - Display VMG before and after maneuvers

### Dashboard View

Display key metrics prominently:

- Race time (total, upwind, downwind)
- Average speed (overall, upwind, downwind)
- Maneuver count (tacks, gybes)

## Technical Requirements

### Frontend

- Web application
- Map visualization: Leaflet
- Data visualization: Matplotlib/Seaborn
- Focus on functionality over flashy features

### Backend

- Python-based (Flask or FastAPI preferred)
- Server-side processing of all data
- PostgreSQL relational database

### Data Processing

- Input format: GPX files (containing location data with timestamps only)
- Manual wind direction input
- Simple moving average for speed/direction smoothing
- Maneuver detection based on direction change >45 degrees
- Error handling for incomplete or corrupted GPX data

## Database Schema

### Users Table

- user_id (PK)
- username
- email
- password (hashed)
- created_at
- last_login

### Races Table

- race_id (PK)
- user_id (FK)
- race_name
- race_date
- gpx_file_path
- wind_direction
- created_at
- updated_at

### RaceMarks Table

- mark_id (PK)
- race_id (FK)
- latitude
- longitude
- mark_type (enum: start, finish, windward, leeward, offset, other)

### RaceSegments Table

- segment_id (PK)
- race_id (FK)
- segment_type (enum: upwind, downwind, reaching)
- start_time
- end_time
- avg_speed
- distance

### Maneuvers Table

- maneuver_id (PK)
- race_id (FK)
- maneuver_type (enum: tack, gybe)
- timestamp
- latitude
- longitude
- speed_before
- speed_after
- speed_loss
- duration

## API Endpoints

### Authentication

- POST /api/register
- POST /api/login
- POST /api/logout

### Race Management

- POST /api/races (upload new race)
- GET /api/races (list user races)
- GET /api/races/{race_id} (get race details)
- DELETE /api/races/{race_id}

### Race Analysis

- POST /api/races/{race_id}/wind (set wind direction)
- POST /api/races/{race_id}/marks (add race mark)
- GET /api/races/{race_id}/analysis (get basic analysis)
- GET /api/races/{race_id}/maneuvers (get maneuver analysis)

## Data Flow

1. **Upload Process**
    - User uploads GPX file
    - Server parses GPX using Python libraries
    - Basic track and timestamp data extracted
    - Data stored in database
    - Server calculates initial metrics (distance, duration)
    - Basic visualization displayed to user
2. **Wind & Course Input**
    - User inputs wind direction via compass
    - User adds course marks by clicking on track
    - Server updates race information in database
3. **Advanced Analysis**
    - Server calculates VMG based on wind direction
    - Server identifies upwind/downwind segments
    - Server detects maneuvers based on course changes
    - Server calculates performance metrics
    - Results displayed in dashboard view

## Implementation Plan

### Phase 1: Core Infrastructure

- Set up Python Flask/FastAPI application
- Implement database schema
- Create user authentication
- Implement GPX file upload and parsing
- Build basic track visualization with Leaflet

### Phase 2: Basic Analysis

- Implement wind direction input interface
- Develop course mark plotting functionality
- Calculate basic metrics (total time, distance)
- Create time slider for race playback

### Phase 3: Advanced Analysis

- Implement upwind/downwind detection
- Calculate VMG
- Detect headers and lifts
- Implement maneuver detection algorithm
- Create maneuver visualization

### Phase 4: Dashboard

- Design and implement metrics dashboard
- Integrate all visualizations
- Implement moving average smoothing
- Finalize UI/UX

## Error Handling Strategy

- Validate GPX files before processing
- For corrupted or incomplete data, display error message to user
- Implement database transaction rollbacks for failed uploads
- Log all errors with context for debugging

## Testing Plan

### Unit Tests

- GPX parsing functionality
- Wind direction calculations
- Maneuver detection algorithm
- VMG calculations
- Course segment identification

### Integration Tests

- File upload workflow
- User authentication flow
- Database operations
- API endpoints

### User Acceptance Testing

- Verify track visualization accuracy
- Validate performance metrics against known data
- Test with various GPX formats and sources
- Verify maneuver detection on different sailing patterns

## Hosting Considerations

- Need to determine hosting solution
- Consider scaling requirements for GPX processing
- Database backups and security
- File storage for GPX files

## Future Enhancements (Not in Initial Scope)

- Mobile compatibility
- Race sharing capability
- Multiple race comparison
- More sophisticated filtering/smoothing algorithms
- Weather data integration
- Performance trending over time