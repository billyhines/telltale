from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.race import Race

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Landing page route"""
    return render_template('index.html')

@main.route('/about')
def about():
    """About page route"""
    return render_template('about.html')

@main.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard for authenticated users"""
    # Get race statistics for the dashboard
    race_count = Race.query.filter_by(user_id=current_user.id).count()
    recent_races = Race.query.filter_by(user_id=current_user.id).order_by(Race.race_date.desc()).limit(5).all()
    
    # Calculate total statistics
    total_distance = 0
    max_speed = 0
    
    for race in Race.query.filter_by(user_id=current_user.id).all():
        if race.total_distance:
            total_distance += race.total_distance
        if race.max_speed and race.max_speed > max_speed:
            max_speed = race.max_speed
    
    return render_template(
        'dashboard.html',
        race_count=race_count,
        recent_races=recent_races,
        total_distance=total_distance,
        max_speed=max_speed
    )

@main.route('/settings')
@login_required
def settings():
    """User settings page"""
    return render_template('settings.html')