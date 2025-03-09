from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import login_required, current_user
from app import db
from app.models.race import Race
from app.forms.race import RaceUploadForm
from app.utils.file_utils import save_gpx_file
import os

races = Blueprint('races', __name__)

@races.route('/races')
@login_required
def list_races():
    """List all races for the current user"""
    user_races = Race.query.filter_by(user_id=current_user.id).order_by(Race.race_date.desc()).all()
    return render_template('races/index.html', races=user_races)

@races.route('/races/upload', methods=['GET', 'POST'])
@login_required
def upload_race():
    """Upload a new race GPX file"""
    form = RaceUploadForm()
    if form.validate_on_submit():
        # Save the GPX file
        success, result = save_gpx_file(form.gpx_file.data, current_user.id)
        
        if not success:
            flash(f'Error uploading file: {result}', 'danger')
            return render_template('races/upload.html', form=form)
        
        # Create new race
        try:
            race = Race.create_from_form(form, current_user.id, result)
            flash('Race uploaded successfully!', 'success')
            return redirect(url_for('races.view_race', race_id=race.race_id))
        except Exception as e:
            flash(f'Error creating race: {str(e)}', 'danger')
    
    return render_template('races/upload.html', form=form)

@races.route('/races/<int:race_id>')
@login_required
def view_race(race_id):
    """View a specific race"""
    race = Race.query.get_or_404(race_id)
    
    # Check if the race belongs to the current user
    if race.user_id != current_user.id:
        flash('You do not have permission to view this race.', 'danger')
        return redirect(url_for('races.list_races'))
    
    return render_template('races/view.html', race=race)

@races.route('/races/<int:race_id>/delete', methods=['POST'])
@login_required
def delete_race(race_id):
    """Delete a race and all associated data"""
    race = Race.query.get_or_404(race_id)
    
    # Check if the race belongs to the current user
    if race.user_id != current_user.id:
        flash('You do not have permission to delete this race.', 'danger')
        return redirect(url_for('races.list_races'))
    
    race_name = race.race_name
    
    if race.delete_with_data():
        flash(f'Race "{race_name}" deleted successfully', 'success')
    else:
        flash(f'Error deleting race', 'danger')
    
    return redirect(url_for('races.list_races'))

@races.route('/api/races/<int:race_id>')
@login_required
def race_json(race_id):
    """Get race data in JSON format"""
    race = Race.query.get_or_404(race_id)
    
    # Check if the race belongs to the current user
    if race.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify(race.to_dict())