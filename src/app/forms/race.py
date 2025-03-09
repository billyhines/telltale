from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Length
from datetime import datetime

class RaceUploadForm(FlaskForm):
    """Form for uploading race GPX files"""
    race_name = StringField('Race Name', 
                           validators=[DataRequired(), Length(min=3, max=128)])
    
    race_date = DateField('Race Date',
                         validators=[DataRequired()],
                         default=datetime.today)
    
    gpx_file = FileField('GPX File', 
                      validators=[
                          FileRequired(),
                          FileAllowed(['gpx'], 'GPX files only!')
                      ])
    
    submit = SubmitField('Upload Race')