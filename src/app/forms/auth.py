from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from app.models.user import User

class LoginForm(FlaskForm):
    """Form for user login"""
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(1, 120)
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    """Form for user registration"""
    username = StringField('Username', validators=[
        DataRequired(),
        Length(3, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must start with a letter and can only contain '
               'letters, numbers, dots or underscores')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(1, 120)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    password2 = PasswordField('Confirm password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

    def validate_email(self, field):
        """Check if email is already registered"""
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        """Check if username is already in use"""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class PasswordResetRequestForm(FlaskForm):
    """Form for requesting a password reset"""
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(1, 120)
    ])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    """Form for resetting password"""
    password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    password2 = PasswordField('Confirm password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Reset Password')