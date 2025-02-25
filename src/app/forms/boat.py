from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange, Length


class BoatForm(FlaskForm):
    """Form for adding and editing boats."""
    name = StringField('Boat Name', validators=[
        DataRequired(), 
        Length(1, 64)
    ])
    boat_type = StringField('Boat Type', validators=[
        DataRequired(), 
        Length(1, 64)
    ])
    length = FloatField('Length (meters)', validators=[
        DataRequired(),
        NumberRange(min=1.0, max=100.0)
    ])
    manufacturer = StringField('Manufacturer', validators=[
        Optional(), 
        Length(0, 64)
    ])
    model = StringField('Model', validators=[
        Optional(), 
        Length(0, 64)
    ])
    year_built = IntegerField('Year Built', validators=[
        Optional(),
        NumberRange(min=1900, max=2100)
    ])
    sail_number = StringField('Sail Number', validators=[
        Optional(), 
        Length(0, 32)
    ])
    hull_id = StringField('Hull ID', validators=[
        Optional(), 
        Length(0, 64)
    ])
    submit = SubmitField('Save Boat')