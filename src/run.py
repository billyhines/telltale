import os
from app import create_app, db
from app.models.user import User
from app.models.boat import Boat
from app.models.race import Race

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    """Make shell context for flask shell command."""
    return {
        'db': db, 
        'User': User, 
        'Boat': Boat, 
        'Race': Race
    }

if __name__ == '__main__':
    app.run(debug=True)