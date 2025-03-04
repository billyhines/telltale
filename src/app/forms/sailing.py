from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class UploadGPXForm(FlaskForm):
    """Form for uploading GPX files"""
    session_name = StringField('Session Name', 
                           validators=[DataRequired(), Length(min=3, max=128)])
    
    gpx_file = FileField('GPX File', 
                      validators=[
                          FileRequired(),
                          FileAllowed(['gpx'], 'GPX files only!')
                      ])
    
    submit = SubmitField('Upload')