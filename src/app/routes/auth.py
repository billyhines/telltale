from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from app.forms.auth import LoginForm, RegistrationForm, PasswordResetRequestForm, PasswordResetForm
import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            # Update last login timestamp
            user.last_login = datetime.datetime.utcnow()
            db.session.commit()
            # Redirect to the page the user was trying to access
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.dashboard')
            return redirect(next_page)
        flash('Invalid email or password.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data.lower(),
            username=form.username.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    """User logout route"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    """Request password reset route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            # In a real application, you would generate a token and send an email
            # For this exercise, we'll just redirect to the reset form directly
            flash('A password reset link has been sent to your email.', 'info')
            return redirect(url_for('auth.login'))
        else:
            flash('Email not found.', 'danger')
    
    return render_template('auth/reset_password_request.html', form=form)

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password with token route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    # In a real application, you would verify the token
    # For this exercise, we'll just show the form
    form = PasswordResetForm()
    if form.validate_on_submit():
        # In a real application, you would get the user from the token
        # For this exercise, we'll just show a success message
        flash('Your password has been updated.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', form=form)

@auth.route('/account')
@login_required
def account():
    """User account settings route"""
    return render_template('auth/account.html')