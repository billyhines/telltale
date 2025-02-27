from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
csrf = CSRFProtect()

def create_app(config_name='default'):
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Ensure upload directory exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Register blueprints
    from app.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from app.routes.sailing import sailing as sailing_blueprint
    app.register_blueprint(sailing_blueprint, url_prefix='/sailing')
    
    # Shell context
    @app.shell_context_processor
    def make_shell_context():
        return dict(
            app=app, 
            db=db, 
            User=User, 
            Race=Race, 
            RaceMark=RaceMark, 
            RaceSegment=RaceSegment,
            Maneuver=Maneuver,
            TrackPoint=TrackPoint
        )
    
    return app

# Import models after db is defined to avoid circular imports
from app.models.user import User
from app.models.race import Race
from app.models.race_mark import RaceMark
from app.models.race_segment import RaceSegment
from app.models.maneuver import Maneuver
from app.models.track_point import TrackPoint