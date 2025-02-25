from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.boat import Boat
from app.models.sailing_session import SailingSession
from app.forms.boat import BoatForm
from app.forms.sailing import SailingSessionForm
from werkzeug.utils import secure_filename
from app.utils.gpx_processor import process_gpx_file
import os
from datetime import datetime

sailing = Blueprint('sailing', __name__)


# Boat routes
@sailing.route('/boats')
@login_required
def boats_list():
    """Show list of user's boats."""
    boats = current_user.boats.all()
    return render_template('sailing/boats_list.html', boats=boats)


@sailing.route('/boats/new', methods=['GET', 'POST'])
@login_required
def new_boat():
    """Add a new boat."""
    form = BoatForm()
    if form.validate_on_submit():
        boat = Boat(
            name=form.name.data,
            boat_type=form.boat_type.data,
            length=form.length.data,
            manufacturer=form.manufacturer.data,
            model=form.model.data,
            year_built=form.year_built.data,
            sail_number=form.sail_number.data,
            hull_id=form.hull_id.data,
            owner=current_user
        )
        db.session.add(boat)
        db.session.commit()
        flash('New boat added successfully!', 'success')
        return redirect(url_for('sailing.boats_list'))
    
    return render_template('sailing/boat_form.html', form=form, title='Add New Boat')


@sailing.route('/boats/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_boat(id):
    """Edit an existing boat."""
    boat = Boat.query.get_or_404(id)
    
    # Check if the current user owns this boat
    if boat.user_id != current_user.id:
        flash('You do not have permission to edit this boat.', 'danger')
        return redirect(url_for('sailing.boats_list'))
    
    form = BoatForm(obj=boat)
    if form.validate_on_submit():
        form.populate_obj(boat)
        db.session.commit()
        flash('Boat details updated successfully!', 'success')
        return redirect(url_for('sailing.boats_list'))
    
    return render_template('sailing/boat_form.html', form=form, title='Edit Boat')


@sailing.route('/boats/<int:id>/delete', methods=['POST'])
@login_required
def delete_boat(id):
    """Delete a boat."""
    boat = Boat.query.get_or_404(id)
    
    # Check if the current user owns this boat
    if boat.user_id != current_user.id:
        flash('You do not have permission to delete this boat.', 'danger')
        return redirect(url_for('sailing.boats_list'))
    
    db.session.delete(boat)
    db.session.commit()
    flash('Boat deleted successfully!', 'success')
    return redirect(url_for('sailing.boats_list'))


# Sailing session routes
@sailing.route('/sessions')
@login_required
def sessions_list():
    """Show list of user's sailing sessions."""
    sessions = SailingSession.query.filter_by(user_id=current_user.id)\
        .order_by(SailingSession.date.desc())\
        .all()
    return render_template('sailing/sessions_list.html', sessions=sessions)


@sailing.route('/sessions/new', methods=['GET', 'POST'])
@login_required
def new_session():
    """Add a new sailing session."""
    form = SailingSessionForm()
    
    # Populate boat choices with user's boats
    form.boat_id.choices = [(boat.id, boat.name) for boat in current_user.boats.all()]
    
    if form.validate_on_submit():
        # Handle GPX file upload
        gpx_filename = None
        if form.gpx_file.data:
            file = form.gpx_file.data
            gpx_filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], gpx_filename)
            file.save(file_path)
            
            # Process GPX file to extract data
            gpx_data = process_gpx_file(file_path)
            
            # Update form data with GPX data if available
            if gpx_data:
                form.distance.data = gpx_data.get('distance', form.distance.data)
                form.max_speed.data = gpx_data.get('max_speed', form.max_speed.data)
                form.avg_speed.data = gpx_data.get('avg_speed', form.avg_speed.data)
        
        # Calculate duration if start and end times are provided
        duration = None
        if form.start_time.data and form.end_time.data:
            duration = int((form.end_time.data - form.start_time.data).total_seconds())
        
        session = SailingSession(
            name=form.name.data,
            date=form.date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            duration=duration,
            distance=form.distance.data,
            max_speed=form.max_speed.data,
            avg_speed=form.avg_speed.data,
            location=form.location.data,
            weather_conditions=form.weather_conditions.data,
            wind_speed=form.wind_speed.data,
            wind_direction=form.wind_direction.data,
            notes=form.notes.data,
            gpx_file=gpx_filename,
            boat_id=form.boat_id.data,
            user_id=current_user.id
        )
        
        db.session.add(session)
        db.session.commit()
        flash('New sailing session added successfully!', 'success')
        return redirect(url_for('sailing.sessions_list'))
    
    return render_template('sailing/session_form.html', form=form, title='Log New Sailing Session')


@sailing.route('/sessions/<int:id>')
@login_required
def view_session(id):
    """View details of a sailing session."""
    session = SailingSession.query.get_or_404(id)
    
    # Check if the current user owns this session
    if session.user_id != current_user.id:
        flash('You do not have permission to view this session.', 'danger')
        return redirect(url_for('sailing.sessions_list'))
    
    return render_template('sailing/session_detail.html', session=session)


@sailing.route('/sessions/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_session(id):
    """Edit an existing sailing session."""
    session = SailingSession.query.get_or_404(id)
    
    # Check if the current user owns this session
    if session.user_id != current_user.id:
        flash('You do not have permission to edit this session.', 'danger')
        return redirect(url_for('sailing.sessions_list'))
    
    form = SailingSessionForm(obj=session)
    
    # Populate boat choices with user's boats
    form.boat_id.choices = [(boat.id, boat.name) for boat in current_user.boats.all()]
    
    if form.validate_on_submit():
        # Handle GPX file upload
        if form.gpx_file.data:
            file = form.gpx_file.data
            gpx_filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], gpx_filename)
            file.save(file_path)
            
            # Process GPX file to extract data
            gpx_data = process_gpx_file(file_path)
            
            # Update form data with GPX data if available
            if gpx_data:
                form.distance.data = gpx_data.get('distance', form.distance.data)
                form.max_speed.data = gpx_data.get('max_speed', form.max_speed.data)
                form.avg_speed.data = gpx_data.get('avg_speed', form.avg_speed.data)
            
            session.gpx_file = gpx_filename
        
        # Calculate duration if start and end times are provided
        if form.start_time.data and form.end_time.data:
            session.duration = int((form.end_time.data - form.start_time.data).total_seconds())
        
        # Update session with form data
        form.populate_obj(session)
        db.session.commit()
        flash('Sailing session updated successfully!', 'success')
        return redirect(url_for('sailing.view_session', id=session.id))
    
    return render_template('sailing/session_form.html', form=form, title='Edit Sailing Session')


@sailing.route('/sessions/<int:id>/delete', methods=['POST'])
@login_required
def delete_session(id):
    """Delete a sailing session."""
    session = SailingSession.query.get_or_404(id)
    
    # Check if the current user owns this session
    if session.user_id != current_user.id:
        flash('You do not have permission to delete this session.', 'danger')
        return redirect(url_for('sailing.sessions_list'))
    
    # Delete associated GPX file if it exists
    if session.gpx_file:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], session.gpx_file)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.session.delete(session)
    db.session.commit()
    flash('Sailing session deleted successfully!', 'success')
    return redirect(url_for('sailing.sessions_list'))


@sailing.route('/analytics')
@login_required
def analytics():
    """Show sailing analytics dashboard."""
    # Get overall sailing statistics
    total_sessions = SailingSession.query.filter_by(user_id=current_user.id).count()
    total_distance = db.session.query(db.func.sum(SailingSession.distance))\
        .filter(SailingSession.user_id == current_user.id)\
        .scalar() or 0
    avg_speed = db.session.query(db.func.avg(SailingSession.avg_speed))\
        .filter(SailingSession.user_id == current_user.id)\
        .scalar() or 0
    max_speed = db.session.query(db.func.max(SailingSession.max_speed))\
        .filter(SailingSession.user_id == current_user.id)\
        .scalar() or 0
    
    # Get sessions by month
    sessions_by_month = db.session.query(
        db.func.strftime('%Y-%m', SailingSession.date).label('month'),
        db.func.count().label('count'),
        db.func.sum(SailingSession.distance).label('distance')
    ).filter(
        SailingSession.user_id == current_user.id
    ).group_by(
        db.func.strftime('%Y-%m', SailingSession.date)
    ).order_by(
        db.func.strftime('%Y-%m', SailingSession.date)
    ).all()
    
    # Get sessions by boat
    sessions_by_boat = db.session.query(
        Boat.name.label('boat_name'),
        db.func.count().label('count'),
        db.func.sum(SailingSession.distance).label('distance'),
        db.func.avg(SailingSession.avg_speed).label('avg_speed')
    ).join(
        Boat, SailingSession.boat_id == Boat.id
    ).filter(
        SailingSession.user_id == current_user.id
    ).group_by(
        SailingSession.boat_id
    ).all()
    
    return render_template(
        'sailing/analytics.html',
        total_sessions=total_sessions,
        total_distance=total_distance,
        avg_speed=avg_speed,
        max_speed=max_speed,
        sessions_by_month=sessions_by_month,
        sessions_by_boat=sessions_by_boat
    )