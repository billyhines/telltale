Sailing Analytics Web App Specification
=======================================

Overview
--------

A sailing analytics application that processes GPX files from sailing races to provide race visualization and maneuver analysis. The application will allow users to upload GPX files, view their sailing tracks on a map, analyze performance metrics, and evaluate maneuvers like tacks and gybes.

Tech Stack
----------

-   **Backend**: FastAPI (Python)
-   **Frontend**: React with React Bootstrap
-   **Data Processing**: Pandas, NumPy, GeoPy, gpxpy
-   **Visualization**: Plotly (charts), Leaflet (maps)
-   **Deployment**: Local application

Architecture
------------

### Backend Components

1.  **FastAPI Server**: Handles API requests, file processing, and analysis
2.  **GPX Parser**: Uses gpxpy to extract track data
3.  **Metrics Calculator**: Derives sailing metrics from raw data
4.  **Maneuver Detector**: Identifies tacks and gybes
5.  **Performance Analyzer**: Evaluates sailing performance around maneuvers

### Frontend Components

1.  **React Application**: Single-page application
2.  **Upload Component**: Handles GPX file uploads
3.  **Map Visualization**: Displays sailing track using Leaflet
4.  **Chart Components**: Displays speed, VMG, etc. using Plotly
5.  **Maneuver Analysis**: Displays performance metrics for maneuvers

Data Flow
---------

1.  User uploads GPX file
2.  Server processes file immediately and returns all basic analysis
3.  User can interact with visualization and maneuver data
4.  User can add course elements (marks, start/finish lines) via the map interface
5.  User can crop race data based on time selection

API Endpoints
-------------

### File Handling

-   **POST /api/upload-and-analyze**
    -   Accepts GPX file upload
    -   Parses file and calculates basic metrics
    -   Detects maneuvers
    -   Returns comprehensive analysis data

### Additional Analysis

-   **POST /api/update-wind-direction**
    -   Updates wind direction and recalculates relevant metrics
-   **POST /api/update-course-elements**
    -   Updates mark positions, start/finish lines
-   **POST /api/crop-race**
    -   Updates analysis based on time selection

Data Models
-----------

### Track Data

-   Latitude
-   Longitude
-   Timestamp
-   Elevation
-   Derived metrics (speed, heading, etc.)

### Analysis Results

-   Summary statistics (distance, time, average speed)
-   Time series data for visualization
-   Maneuver data (positions, timestamps, performance metrics)

### Course Elements

-   Mark positions
-   Start/finish line coordinates
-   Wind direction

Key Features
------------

### Visualization Tab

-   Interactive map showing sailing track
-   Speed, VMG, and other metrics plotted over time
-   Summary statistics display
-   User input for wind direction
-   Visual placement of course elements (marks, start/finish lines)
-   Time-based race cropping

### Maneuver Analysis Tab

-   List of detected maneuvers (tacks, gybes)
-   Performance metrics for each maneuver:
    -   Speed 10s before and after
    -   VMG 10s before and after
    -   Distance lost during maneuver
-   Both automatic detection and manual marking of maneuvers

Processing Logic
----------------

### Speed Calculation

-   Calculate speed from sequential position and timestamp data

### VMG Calculation

-   Calculate using speed and wind angle relative to course

### True Wind Angle

-   Calculate using boat speed and user-provided wind direction

### Maneuver Detection

-   Identify significant heading changes (tacks)
-   Use combination of heading and speed patterns for gybes
-   Allow manual correction/addition of maneuvers

User Interface Design
---------------------

### Main Layout

-   Navigation with two tabs (Visualization and Maneuver Analysis)
-   File upload area
-   Controls for wind direction and course elements
-   Time-based race selector

### Visualization Tab

-   Map display with track
-   Chart displays for speed, VMG, etc.
-   Summary statistics
-   Course element controls

### Maneuver Analysis Tab

-   List of maneuvers
-   Performance metrics for selected maneuver
-   Charts showing before/after comparison

Error Handling
--------------

-   Basic validation of GPX files (format, required fields)
-   User-friendly error messages for invalid inputs
-   Fallback visualizations when data is insufficient

Performance Considerations
--------------------------

-   Synchronous processing for simplicity
-   Optimize calculations for common racing analytics
-   Consider memory usage for larger GPX files

Development Roadmap
-------------------

### Phase 1: Core Functionality

1.  Set up FastAPI backend with file upload and parsing
2.  Implement basic metrics calculation
3.  Create React frontend with map visualization
4.  Implement summary statistics display

### Phase 2: Advanced Features

1.  Implement maneuver detection algorithm
2.  Add performance analysis for maneuvers
3.  Add course element placement
4.  Implement time-based race cropping

### Phase 3: Refinement

1.  Improve UI/UX
2.  Optimize performance
3.  Address edge cases and improve error handling

Testing Strategy
----------------

-   Unit tests for calculation functions
-   API tests for endpoints
-   Sample GPX files for integration testing
-   Browser testing for frontend components

This specification provides a comprehensive guide for developing the sailing analytics web application as discussed. The application will enable sailors to analyze their race performance through visualization and maneuver analysis, with a focus on simplicity and usability.