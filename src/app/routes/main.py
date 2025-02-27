from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from app.models.race import Race

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """Render the home page."""
    return render_template('main/index.html')


@main.route('/dashboard')
@login_required
def dashboard():
    """Render the user dashboard with sailing analytics."""
    # Get user's recent sailing sessions
    recent_sessions = Race.query.filter_by(user_id=current_user.id)\
        .order_by(Race.race_date.desc())\
        .limit(5)\
        .all()
    
    # Calculate total stats
    total_sessions = Race.query.filter_by(user_id=current_user.id).count()
    total_distance = Race.query.filter_by(user_id=current_user.id)\
        .with_entities(Race.distance)\
        .all()
    total_distance = sum([d[0] for d in total_distance if d[0] is not None])
    
    # Get user's boats
    boats = current_user.boats.all()
    
    return render_template(
        'main/dashboard.html',
        recent_sessions=recent_sessions,
        total_sessions=total_sessions,
        total_distance=total_distance,
        boats=boats
    )


@main.route('/about')
def about():
    """Render the about page."""
    return render_template('main/about.html')