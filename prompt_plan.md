Sailing Analytics Platform Implementation Plan
==============================================

Based on the specification document, I've created a detailed implementation plan divided into manageable steps. Each step builds incrementally on the previous ones to create a complete sailing analytics platform.

Implementation Blueprint
------------------------

### Phase 1: Project Foundation

1.  Set up development environment and project structure
2.  Create database models and migrations
3.  Implement authentication system
4.  Build basic frontend structure

### Phase 2: Data Handling

1.  Implement GPX upload and storage
2.  Create GPX parsing functionality
3.  Set up basic map visualization
4.  Add speed visualization with color gradient

### Phase 3: Race Analysis Features

1.  Implement time slider for race playback
2.  Create wind direction input interface
3.  Add race mark plotting capability
4.  Calculate basic race metrics
5.  Implement upwind/downwind detection
6.  Calculate and visualize VMG
7.  Detect headers and lifts

### Phase 4: Advanced Analysis

1.  Build maneuver detection algorithm
2.  Calculate maneuver performance metrics
3.  Create maneuver visualization overlay
4.  Implement dashboard for key metrics
5.  Add comprehensive error handling

Implementation Prompts
----------------------

Each prompt below is designed to guide an LLM through implementing one specific component of the system, building incrementally on previous steps.

### Prompt 1: Project Setup and Structure

```
Create a new Flask project for a Sailing Analytics Platform. Set up the initial directory structure following best practices with separation of concerns:

1. Create a virtual environment and generate requirements.txt with these dependencies:
   - Flask
   - SQLAlchemy
   - Flask-SQLAlchemy
   - Flask-Migrate
   - Flask-Login
   - Flask-WTF
   - psycopg2-binary
   - gpxpy (for parsing GPX files)

2. Create the following directory structure:
   - app/
     - __init__.py (Flask application factory)
     - models/
     - routes/
     - templates/
     - static/
     - utils/
   - migrations/
   - config.py
   - run.py

3. In config.py, set up configuration classes for development, testing, and production environments.

4. In app/__init__.py, create an application factory that initializes Flask extensions.

5. In run.py, create code to run the application.

Provide all necessary code for these files to set up a working Flask application structure.

```

### Prompt 2: Database Models

```
For our Sailing Analytics Platform, create SQLAlchemy models based on the following requirements:

1. In app/models/__init__.py, set up SQLAlchemy instance.

2. Create the following models in separate files:
   - User model (app/models/user.py) with:
     - user_id (PK)
     - username
     - email
     - password_hash
     - created_at
     - last_login
     - races relationship

   - Race model (app/models/race.py) with:
     - race_id (PK)
     - user_id (FK)
     - race_name
     - race_date
     - gpx_file_path
     - wind_direction
     - created_at
     - updated_at
     - marks relationship
     - segments relationship
     - maneuvers relationship

   - RaceMark model (app/models/race_mark.py) with:
     - mark_id (PK)
     - race_id (FK)
     - latitude
     - longitude
     - mark_type (enum: start, finish, windward, leeward, offset, other)

   - RaceSegment model (app/models/race_segment.py) with:
     - segment_id (PK)
     - race_id (FK)
     - segment_type (enum: upwind, downwind, reaching)
     - start_time
     - end_time
     - avg_speed
     - distance

   - Maneuver model (app/models/maneuver.py) with:
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

3. Create a TrackPoint model to store the parsed GPX data:
   - point_id (PK)
   - race_id (FK)
   - latitude
   - longitude
   - timestamp
   - speed (calculated)
   - heading (calculated)
   - vmg (nullable, calculated later)

4. Set up appropriate relationships between models.

5. Include helper methods for each model to assist with common operations.

6. Update app/__init__.py to include the database configuration.

Ensure proper indexing for performance and include appropriate __repr__ methods for debugging.

```

### Prompt 3: Authentication System

```
Implement a complete authentication system for the Sailing Analytics Platform using Flask-Login:

1. Update the User model to work with Flask-Login:
   - Add user_loader callback
   - Implement methods for password hashing and verification using werkzeug.security
   - Add is_authenticated, is_active, is_anonymous, and get_id methods

2. Create authentication forms using Flask-WTF:
   - Registration form with username, email, password, and confirmation fields
   - Login form with email/username and password fields
   - Password reset form

3. Create authentication routes in app/routes/auth.py:
   - /register - for user registration
   - /login - for user login
   - /logout - for user logout
   - /reset-password - for password reset

4. Create HTML templates for authentication:
   - register.html
   - login.html
   - reset_password.html

5. Update app/__init__.py to include Flask-Login initialization

6. Create a basic navigation template that shows login/logout based on authentication status

7. Add login_required decorators where appropriate to protect routes

8. Set up error handling for authentication failures

Use secure practices throughout, including:
- CSRF protection
- Secure password storage
- Rate limiting for login attempts
- Proper session management

```

### Prompt 4: Frontend Structure

```
Create the frontend structure for the Sailing Analytics Platform using Flask templates, Bootstrap, and appropriate JavaScript libraries:

1. Set up a base layout template (templates/base.html) that includes:
   - Bootstrap 5 CSS and JS
   - Navigation bar
   - Flash messages display
   - Content block
   - Footer

2. Create a dashboard layout (templates/dashboard.html) that extends the base layout with:
   - Sidebar for navigation
   - Main content area with cards/panels
   - User information display

3. Create a home page (templates/index.html) with:
   - Platform introduction
   - Features overview
   - Login/Register buttons for unauthenticated users
   - Quick access to races for authenticated users

4. Set up the static directory structure:
   - static/css/ - for custom CSS files
   - static/js/ - for JavaScript files
   - static/images/ - for image assets

5. Create a custom.css file with styling specific to the sailing platform

6. Create a custom.js file with common JavaScript functions

7. Add route in app/routes/main.py for the home page

8. Update app/__init__.py to register the main blueprint

Make sure the frontend is responsive and provides a clean, professional appearance suitable for data analysis. Include appropriate navigation between pages and ensure all UI elements follow a consistent design language.

```

### Prompt 5: Race Upload Functionality

```
Implement the race upload functionality for the Sailing Analytics Platform:

1. Create a race management blueprint (app/routes/races.py) with routes:
   - GET /races - list user's races
   - GET /races/<race_id> - view a specific race
   - POST /races - upload a new race
   - DELETE /races/<race_id> - delete a race

2. Create race upload form using Flask-WTF with fields:
   - race_name
   - race_date
   - gpx_file (FileField)

3. Create race list and detail templates:
   - templates/races/index.html - list of user's races
   - templates/races/upload.html - form to upload a new race
   - templates/races/view.html - detail view of a race (placeholder for now)

4. Create a utility function in app/utils/file_utils.py to:
   - Validate uploaded GPX files
   - Save files to a secure location with unique filenames
   - Handle errors during upload

5. Update the Race model to include:
   - Method to create a new race from form data
   - Method to delete a race and associated files
   - Property to get full path to GPX file

6. Create a RaceSchema using Marshmallow for serializing race data to JSON

7. Register the races blueprint in app/__init__.py

8. Update the navigation to include race management links

Ensure proper validation of inputs, secure file handling, and appropriate error messages for the user. Only authenticated users should be able to access race management features.

```

### Prompt 6: GPX Parsing

```
Implement GPX file parsing functionality for the Sailing Analytics Platform:

1. Create a GPX parser utility in app/utils/gpx_parser.py that:
   - Uses gpxpy to parse uploaded GPX files
   - Extracts track points with timestamps, latitude, and longitude
   - Calculates speed between consecutive points
   - Calculates heading between consecutive points
   - Handles errors in GPX data gracefully
   - Returns data in a format ready for database insertion

2. Create a background task function that:
   - Takes a race_id as input
   - Loads the associated GPX file
   - Parses the GPX data
   - Stores parsed points in the TrackPoint model
   - Updates the Race model with stats (duration, distance, etc.)
   - Marks the race as processed

3. Update the Race model to include:
   - is_processed flag
   - processing_error field for error messages
   - Statistics fields (total_distance, duration, max_speed, avg_speed)
   - Method to trigger background processing
   - Method to check processing status

4. Add an endpoint to the races blueprint:
   - GET /races/<race_id>/status - returns processing status

5. Update the race upload functionality to:
   - Trigger GPX processing after successful upload
   - Redirect to a page showing processing status

6. Create a simple template to show processing status:
   - templates/races/processing.html

7. Add JavaScript to the processing template to poll the status endpoint

Ensure proper error handling throughout the process and provide meaningful feedback to the user. Consider potential issues with large GPX files and implement appropriate optimizations.

```

### Prompt 7: Basic Map Visualization

```
Implement basic map visualization for the Sailing Analytics Platform using Leaflet.js:

1. Add Leaflet.js dependencies to the base template:
   - Leaflet CSS
   - Leaflet JavaScript

2. Create a map display component in static/js/map.js:
   - Initialize a Leaflet map in a container
   - Set up map controls (zoom, layers)
   - Configure base map tiles (OpenStreetMap or similar)
   - Function to display a track on the map
   - Function to fit map bounds to track
   - Function to clear map layers

3. Update the race detail template (templates/races/view.html):
   - Add a div container for the map
   - Include necessary JavaScript
   - Add basic race information display

4. Add an API endpoint to the races blueprint:
   - GET /api/races/<race_id>/track - returns track points

5. Create a TrackPointSchema using Marshmallow for serializing track data to GeoJSON

6. Update the TrackPoint model to include a method to convert to GeoJSON

7. Implement client-side JavaScript to:
   - Fetch track data from API
   - Convert data to Leaflet format
   - Display track on the map
   - Center and zoom map appropriately

8. Add basic controls to the map interface:
   - Toggle map layers
   - Reset view button

9. Update the race detail route to include necessary data for the map

Ensure the map interface is responsive and works well on different screen sizes. Include error handling for cases where track data cannot be loaded or displayed.

```

### Prompt 8: Speed Visualization

```
Enhance the map visualization with speed-based coloring for the Sailing Analytics Platform:

1. Update the TrackPoint model to ensure speed is calculated and stored:
   - If speed is not in the GPX data, calculate it between points
   - Add method to retrieve min/max speeds for a race

2. Modify the track API endpoint to include speed data:
   - Update /api/races/<race_id>/track to include speed for each point
   - Add min/max speed data in the response metadata

3. Create a color utility in static/js/color-utils.js:
   - Function to convert speed to a color on a blue-to-red gradient
   - Function to generate a color legend based on min/max speeds

4. Update map.js to implement speed-based visualization:
   - Use polylines with different colors based on speed
   - Split track into segments based on speed ranges
   - Display color legend on the map

5. Add a speed legend component to the race view template:
   - Display color gradient
   - Show min/max speed values
   - Allow toggling legend visibility

6. Implement a speed display that shows:
   - Current speed at selected point
   - Average speed for the race
   - Maximum speed for the race

7. Add styling for the speed visualization components

8. Ensure mobile compatibility for all new components

Make sure the color gradient provides good visual distinction between different speeds and is intuitive for users (blue for slower, red for faster). Use appropriate units (knots) for speed display and allow for unit conversion if needed.

```

### Prompt 9: Time Slider Implementation

```
Implement a time slider for race playback in the Sailing Analytics Platform:

1. Add required JavaScript libraries to the base template:
   - noUiSlider or similar for the slider component
   - moment.js for time handling

2. Create a time slider component in static/js/time-slider.js:
   - Initialize slider with race start/end times
   - Include play, pause, and reset buttons
   - Add speed control for playback (1x, 2x, 4x)
   - Function to update map based on slider position
   - Time display showing current playback time

3. Update the race detail template (templates/races/view.html):
   - Add container for the time slider
   - Add playback controls
   - Add current time display

4. Update map.js to support time-based visualization:
   - Add a "current position" marker
   - Function to show track up to a specific time
   - Function to animate boat position during playback

5. Implement client-side state management:
   - Store current playback state (playing, paused)
   - Store current playback speed
   - Store current timestamp

6. Add styling for the time slider and controls in custom.css

7. Ensure the time slider updates correctly when:
   - User drags the slider
   - Playback is running
   - User clicks on the track to select a specific time

8. Add a time display that shows:
   - Current time in race
   - Elapsed time
   - Remaining time

Make sure the time slider is responsive and works well on different screen sizes. Implement smooth animations for the boat position during playback and ensure good performance even with large tracks.

```

### Prompt 10: Wind Direction Input

```
Implement wind direction input functionality for the Sailing Analytics Platform:

1. Create a visual compass selector component in static/js/wind-compass.js:
   - Canvas-based or SVG-based compass rose
   - Interactive arrow that can be rotated by dragging
   - Numerical display of wind direction in degrees
   - Function to set initial wind direction
   - Event handlers for user interaction

2. Update the race detail template (templates/races/view.html):
   - Add container for the wind compass
   - Add numerical input for direct degree entry
   - Add save button for wind direction

3. Create an API endpoint in the races blueprint:
   - PUT /api/races/<race_id>/wind - updates wind direction

4. Update the Race model:
   - Add validation for wind direction (0-359 degrees)
   - Update wind_direction field when API is called

5. Add client-side JavaScript to:
   - Initialize compass with saved wind direction
   - Update numerical display when compass is rotated
   - Update compass when numerical input changes
   - Save wind direction to the server
   - Show success/error messages after saving

6. Add styling for the wind compass in custom.css

7. Ensure the compass is responsive and works well on different screen sizes

8. Add a visual indicator on the map showing wind direction

9. Update the race detail page to display the saved wind direction

Make sure the wind compass provides intuitive interaction for sailors and displays wind direction in a way that matches sailing conventions (direction wind is coming FROM, not going TO).

```

### Prompt 11: Race Mark Plotting

```
Implement race mark plotting functionality for the Sailing Analytics Platform:

1. Create a RaceMark management component in static/js/race-marks.js:
   - Functions to add, edit, and delete marks
   - Support for different mark types (start, finish, windward, leeward, etc.)
   - Drag-and-drop functionality for mark positioning
   - Visual display of marks on the map with appropriate icons

2. Create API endpoints in the races blueprint:
   - POST /api/races/<race_id>/marks - adds a new mark
   - PUT /api/races/<race_id>/marks/<mark_id> - updates a mark
   - DELETE /api/races/<race_id>/marks/<mark_id> - deletes a mark
   - GET /api/races/<race_id>/marks - gets all marks for a race

3. Create a RaceMarkSchema using Marshmallow for serializing mark data

4. Update the race detail template (templates/races/view.html):
   - Add controls for mark management
   - Add mark type selector
   - Add mark list display

5. Update map.js to support mark visualization:
   - Custom icons for different mark types
   - Click handlers for adding marks at specific locations
   - Popup information for marks

6. Implement client-side JavaScript to:
   - Fetch and display existing marks
   - Allow adding new marks by clicking on the map
   - Edit mark details via popup
   - Delete marks
   - Save changes to the server

7. Add styling for the mark controls and displays

8. Ensure mark editing works well on mobile devices

Make sure the mark plotting is intuitive for sailors and provides clear visual indication of the race course. Include appropriate validation to prevent invalid mark configurations.

```

### Prompt 12: Basic Metrics Calculation

```
Implement basic race metrics calculation for the Sailing Analytics Platform:

1. Create a race analysis utility in app/utils/race_analysis.py to calculate:
   - Total race time (from first to last point)
   - Total distance sailed
   - Average speed
   - Maximum speed
   - Time spent sailing (excluding stationary periods)
   - Distance made good (straight line from start to finish)
   - Efficiency ratio (distance made good / distance sailed)

2. Update the Race model to store calculated metrics:
   - Add fields for each calculated metric
   - Add method to trigger metrics calculation
   - Add method to retrieve formatted metrics

3. Create an API endpoint in the races blueprint:
   - GET /api/races/<race_id>/metrics - returns all calculated metrics

4. Create a metrics display component for the frontend:
   - Card-based layout for key metrics
   - Appropriate units and formatting
   - Simple data visualizations (gauges, charts)

5. Update the race detail template to include the metrics display

6. Implement client-side JavaScript to:
   - Fetch metrics data from API
   - Update metrics display
   - Handle refresh when data changes

7. Add a "Recalculate" button to trigger metrics update

8. Add styling for the metrics display components

9. Ensure the metrics are updated when related data changes (e.g., after adding marks)

Make sure the metrics are meaningful for sailors and presented in an intuitive way. Use appropriate sailing units (knots for speed, nautical miles for distance) and provide clear labels.

```

### Prompt 13: Upwind/Downwind Detection

```
Implement upwind/downwind segment detection for the Sailing Analytics Platform:

1. Enhance the race analysis utility in app/utils/race_analysis.py to:
   - Calculate boat heading at each point
   - Determine if a segment is upwind, downwind, or reaching based on wind direction
   - Define upwind as sailing within 45° of wind direction
   - Define downwind as sailing within 45° of opposite wind direction
   - Define reaching as anything else
   - Group consecutive points into segments of the same type
   - Calculate segment statistics (duration, distance, avg speed)

2. Create methods in the RaceSegment model:
   - Create segments from analysis results
   - Get all segments for a race
   - Calculate aggregate statistics by segment type

3. Create API endpoints in the races blueprint:
   - POST /api/races/<race_id>/analyze - triggers segment analysis
   - GET /api/races/<race_id>/segments - returns all segments

4. Create a RaceSegmentSchema using Marshmallow for serializing segment data

5. Update map.js to support segment visualization:
   - Color-code track sections by segment type (upwind/downwind/reaching)
   - Add legend for segment types
   - Add option to filter display by segment type

6. Create a segment analysis component for the frontend:
   - Display segment statistics in a table
   - Show time and distance percentage for each segment type
   - Compare speeds across different segment types

7. Update the race detail template to include:
   - Segment analysis display
   - Controls to trigger analysis
   - Segment filtering options

8. Implement client-side JavaScript to:
   - Fetch segment data from API
   - Update segment display
   - Filter map display based on segment type

Make sure the segment detection provides meaningful analysis for sailors and accurately represents upwind/downwind sailing based on the provided wind direction.

```

### Prompt 14: VMG Calculation and Visualization

```
Implement Velocity Made Good (VMG) calculation and visualization for the Sailing Analytics Platform:

1. Enhance the race analysis utility in app/utils/race_analysis.py to:
   - Calculate VMG for each track point based on wind direction
   - Determine optimal upwind and downwind VMG angles
   - Calculate VMG efficiency (actual VMG / theoretical optimal VMG)
   - Find best and worst VMG segments

2. Update the TrackPoint model:
   - Add field for VMG
   - Add method to calculate VMG for all points in a race
   - Update API to include VMG in track data

3. Update the RaceSegment model:
   - Add average VMG for each segment
   - Add VMG efficiency percentage

4. Create API endpoints:
   - GET /api/races/<race_id>/vmg - returns VMG data
   - GET /api/races/<race_id>/vmg/optimal - returns optimal VMG angles

5. Update map.js to support VMG visualization:
   - Add option to color-code track by VMG instead of speed
   - Add VMG color gradient legend
   - Highlight best and worst VMG sections

6. Create a VMG analysis component for the frontend:
   - Display current VMG at selected point
   - Show optimal VMG angles for current wind
   - Visualize VMG efficiency with gauges or charts
   - Compare upwind and downwind VMG performance

7. Update the race detail template to include:
   - VMG analysis display
   - Toggle between speed and VMG visualization
   - VMG efficiency indicators

8. Add styling for the VMG visualization components

Make sure the VMG calculation uses proper sailing physics and provides meaningful insights for sailors. Include appropriate explanations of VMG concepts for less experienced users.

```

### Prompt 15: Headers and Lifts Detection

```
Implement headers and lifts detection for the Sailing Analytics Platform:

1. Enhance the race analysis utility in app/utils/race_analysis.py to:
   - Calculate wind angle relative to boat heading at each point
   - Detect significant changes in relative wind angle
   - Identify headers (unfavorable wind shifts) and lifts (favorable wind shifts)
   - Calculate the impact of each shift on performance
   - Identify optimal tack/gybe moments

2. Create a WindShift model to store detected shifts:
   - shift_id (PK)
   - race_id (FK)
   - timestamp
   - latitude
   - longitude
   - shift_type (enum: header, lift)
   - magnitude (degrees)
   - duration
   - impact (performance gain/loss)

3. Create API endpoints:
   - POST /api/races/<race_id>/analyze/shifts - triggers shift analysis
   - GET /api/races/<race_id>/shifts - returns detected shifts

4. Create a WindShiftSchema using Marshmallow for serializing shift data

5. Update map.js to support shift visualization:
   - Add markers for headers and lifts on the map
   - Use different icons/colors for headers vs. lifts
   - Add popup information for each shift

6. Create a shift analysis component for the frontend:
   - Display shifts in a table with details
   - Show shift impact on performance
   - Provide recommendations for optimal tacking strategy

7. Update the race detail template to include:
   - Shift analysis display
   - Controls to trigger shift analysis
   - Option to show/hide shift markers

8. Implement client-side JavaScript to:
   - Fetch shift data from API
   - Update shift display
   - Filter shift display by type or magnitude

Make sure the shift detection uses proper sailing tactics knowledge and provides actionable insights for improving race performance. Include appropriate explanations of headers and lifts concepts.

```

### Prompt 16: Maneuver Detection

```
Implement maneuver detection (tacks and gybes) for the Sailing Analytics Platform:

1. Enhance the race analysis utility in app/utils/race_analysis.py to:
   - Detect significant course changes (>45 degrees)
   - Classify maneuvers as tacks or gybes based on wind direction
   - Identify the exact moment of maneuver
   - Calculate maneuver duration
   - Determine start and end points of each maneuver

2. Create methods in the Maneuver model:
   - Create maneuvers from detection results
   - Get all maneuvers for a race
   - Calculate aggregate statistics by maneuver type

3. Create API endpoints:
   - POST /api/races/<race_id>/analyze/maneuvers - triggers maneuver detection
   - GET /api/races/<race_id>/maneuvers - returns all detected maneuvers

4. Create a ManeuverSchema using Marshmallow for serializing maneuver data

5. Update map.js to support maneuver visualization:
   - Add markers for maneuvers on the map
   - Use different icons for tacks vs. gybes
   - Highlight the maneuver path on the map
   - Add popup information for each maneuver

6. Create a maneuver list component for the frontend:
   - Display maneuvers in a table with details
   - Show count of each maneuver type
   - Allow sorting/filtering of maneuvers

7. Update the race detail template to include:
   - Maneuver list display
   - Controls to trigger maneuver detection
   - Option to show/hide maneuver markers

8. Implement client-side JavaScript to:
   - Fetch maneuver data from API
   - Update maneuver display
   - Highlight maneuvers on map when selected in the list

Make sure the maneuver detection is accurate and accounts for GPS noise. Include appropriate threshold adjustments to prevent false positives.

```

### Prompt 17: Maneuver Performance Analysis

```
Implement maneuver performance analysis for the Sailing Analytics Platform:

1. Enhance the maneuver detection in app/utils/race_analysis.py to:
   - Calculate boat speed before, during, and after maneuvers
   - Determine speed loss during maneuvers
   - Calculate time to recover to previous speed
   - Estimate efficiency of each maneuver
   - Compare maneuver performance to user's average

2. Update the Maneuver model:
   - Add fields for performance metrics
   - Add method to calculate performance for all maneuvers
   - Add method to get best and worst maneuvers

3. Create API endpoints:
   - GET /api/races/<race_id>/maneuvers/performance - returns performance data
   - GET /api/races/<race_id>/maneuvers/best - returns best maneuvers
   - GET /api/races/<race_id>/maneuvers/worst - returns worst maneuvers

4. Update the ManeuverSchema to include performance data

5. Create a maneuver performance component for the frontend:
   - Display performance metrics for each maneuver
   - Compare maneuvers with average performance
   - Highlight best and worst maneuvers
   - Show speed loss visualization

6. Update the maneuver list to include:
   - Speed loss column
   - Recovery time column
   - Efficiency rating
   - Color coding based on performance

7. Create a detailed view for individual maneuvers:
   - Speed graph before/during/after maneuver
   - Comparison to optimal maneuver
   - Specific improvement suggestions

8. Implement client-side JavaScript to:
   - Fetch detailed performance data for selected maneuver
   - Update performance display
   - Generate performance visualizations

Make sure the performance analysis provides actionable insights for improving maneuver technique. Use appropriate sailing terminology and concepts familiar to the target audience.

```

### Prompt 18: Maneuver Visualization Overlay

```
Implement a maneuver visualization overlay for the Sailing Analytics Platform:

1. Create a specialized visualization utility in app/utils/maneuver_visualization.py to:
   - Extract data for maneuver comparison
   - Normalize maneuvers to a common reference frame
   - Calculate aggregate statistics for maneuvers
   - Generate data for visualization

2. Create API endpoints:
   - GET /api/races/<race_id>/maneuvers/overlay - returns data for visualization
   - GET /api/races/<race_id>/maneuvers/<maneuver_id>/detail - returns detailed data for a specific maneuver

3. Create a visualization component in static/js/maneuver-overlay.js:
   - Canvas or SVG-based visualization
   - Display multiple maneuvers overlaid on same graph
   - Show aggregate averages as bold lines
   - Show individual maneuvers as dotted lines
   - Center all visualizations at maneuver point (0 on time axis)
   - Display VMG before and after maneuvers

4. Create a maneuver comparison template:
   - templates/races/maneuver_comparison.html
   - Include visualization container
   - Add controls for filtering maneuvers
   - Add options for different visualization modes

5. Add a route to the races blueprint for the comparison view:
   - GET /races/<race_id>/maneuvers/compare

6. Update the race detail template to include a link to the comparison view

7. Implement client-side JavaScript to:
   - Fetch overlay data from API
   - Generate the visualization
   - Update based on user filter selections
   - Highlight specific maneuvers on hover/select

8. Add styling for the visualization components

Make sure the visualization is intuitive and provides clear insights into maneuver technique. Use appropriate scaling and normalization to make different maneuvers comparable.

```

### Prompt 19: Dashboard Implementation

```
Implement a comprehensive dashboard for the Sailing Analytics Platform:

1. Create a dashboard template (templates/dashboard.html) that includes:
   - Summary of user's sailing activity
   - Recent races list
   - Key performance metrics across all races
   - Quick links to detailed analysis views

2. Create a dashboard controller in app/routes/dashboard.py with routes:
   - GET /dashboard - main dashboard view
   - GET /api/dashboard/summary - returns summary data
   - GET /api/dashboard/recent-races - returns recent races
   - GET /api/dashboard/performance - returns performance metrics

3. Create dashboard utility in app/utils/dashboard_utils.py to:
   - Calculate aggregate statistics across races
   - Generate performance trends over time
   - Identify areas for improvement
   - Prepare data for dashboard visualization

4. Create dashboard components in static/js/dashboard.js:
   - Activity summary chart
   - Performance metrics display
   - Recent races table
   - Performance trends visualization

5. Implement client-side JavaScript to:
   - Fetch dashboard data from API
   - Update dashboard components
   - Handle refresh when data changes

6. Add navigation links to the dashboard from other parts of the application

7. Create mobile-friendly layouts for dashboard components

8. Add customization options:
   - Filter by date range
   - Filter by race type
   - Change visualization settings

Make sure the dashboard provides a clear overview of the user's sailing performance and highlights the most important insights. Design for quick understanding while providing paths to more detailed analysis.

```

### Prompt 20: Error Handling and Integration

```
Implement comprehensive error handling and final integration for the Sailing Analytics Platform:

1. Create a centralized error handling system:
   - Custom exception classes for different error types
   - Error logging with appropriate detail
   - User-friendly error messages
   - API error responses with consistent format

2. Implement error handling for:
   - GPX file parsing issues
   - Invalid wind direction input
   - Missing data for calculations
   - Database operation failures
   - Authentication and authorization errors

3. Create an error display component for the frontend:
   - Show appropriate error messages
   - Provide guidance on fixing issues
   - Include retry options where applicable

4. Add validation:
   - Client-side validation for all forms
   - Server-side validation for all inputs
   - Data consistency checks

5. Implement transaction management:
   - Ensure database operations are atomic
   - Roll back failed operations
   - Prevent data corruption

6. Create a system status component:
   - Show processing status for long operations
   - Indicate when data is being refreshed
   - Display system notifications

7. Optimize performance:
   - Add database indexes for common queries
   - Implement caching for expensive calculations
   - Optimize API response formats

8. Conduct integration testing:
   - Verify all components work together
   - Test with various GPX file formats
   - Ensure consistent behavior across browsers

9. Create a final user guide:
   - Explain all features
   - Provide usage examples
   - Include troubleshooting section

Make sure the application is robust, handles errors gracefully, and provides a smooth user experience even when things go wrong. Focus on guiding the user through the process with clear feedback at each step.

```

Each prompt builds incrementally on the previous ones, ensuring a cohesive development process with no orphaned code. The steps are sized to make meaningful progress while remaining manageable for implementation.