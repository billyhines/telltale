import os
from app import create_app, db
from app.models import User  # Import your models here

# Create app instance based on environment variable or default to development
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    """Add database and models to flask shell context"""
    return {
        'db': db,
        'User': User,
        # Add more models as they are created
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)