from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, FloatField, TextAreaField, DateField, SelectField
from wtforms import TimeField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange, Length
from datetime import datetime


class SailingSessionForm(FlaskForm):
    """Form for adding and editing sailing sessions."""
    name = StringField('Session Name', validators=[
        DataRequired(),
        Length(1, 128)
    ])
    date = DateField('Date', validators=[
        DataRequired()
    ], default=datetime.today)
    start_time = TimeField('Start Time', validators=[Optional()], format='%H:%M')
    end_time = TimeField('End Time', validators=[Optional()], format='%H:%M')
    location = StringField('Location', validators=[
        Optional(),
        Length(0, 128)
    ])
    boat_id = SelectField('Boat', coerce=int, validators=[DataRequired()])
    distance = FloatField('Distance (nautical miles)', validators=[
        Optional(),
        NumberRange(min=0)
    ])
    max_speed = FloatField('Maximum Speed (knots)', validators=[
        Optional(),
        NumberRange(min=0)
    ])
    avg_speed = FloatField('Average Speed (knots)', validators=[
        Optional(),
        NumberRange(min=0)
    ])
    weather_conditions = StringField('Weather Conditions', validators=[
        Optional(),
        Length(0, 256)
    ])
    wind_speed = FloatField('Wind Speed (knots)', validators=[
        Optional(),
        NumberRange(min=0)
    ])
    wind_direction = SelectField('Wind Direction', choices=[
        ('', 'Select Direction'),
        ('N', 'North'),
        ('NE', 'Northeast'),
        ('E', 'East'),
        ('SE', 'Southeast'),
        ('S', 'South'),
        ('SW', 'Southwest'),
        ('W', 'West'),
        ('NW', 'Northwest')
    ], validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional()])
    gpx_file = FileField('GPX Track File', validators=[
        Optional(),
        FileAllowed(['gpx'], 'GPX files only!')
    ])
    submit = SubmitField('Save Session')