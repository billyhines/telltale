# Sailing Analytics Platform

A Flask-based web application for tracking and analyzing sailing sessions.

## Features

- User authentication and profile management
- Boat management for multiple vessels
- Sailing session tracking with detailed analytics
- GPX file upload and analysis
- Performance metrics for sailing improvement
- Interactive dashboard with visualizations

## Directory Structure

```
sailing-analytics/
├── app/
│   ├── __init__.py           # Application factory
│   ├── models/               # Database models
│   ├── routes/               # Route handlers
│   ├── templates/            # Jinja2 templates
│   ├── static/               # CSS, JS, images
│   └── utils/                # Utility functions
├── migrations/               # Database migrations
├── config.py                 # Configuration settings
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Setup Instructions

### 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a .env file

Create a `.env` file in the project root with the following variables:

```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DEV_DATABASE_URL=sqlite:///sailing-dev.db
```

### 4. Initialize the database

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Run the application

```bash
flask run
```

The application will be available at http://127.0.0.1:5000/

## Development

### Database Migrations

After making changes to the models, create a new migration:

```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

### Testing

Run tests with:

```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.