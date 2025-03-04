from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
# We'll create these forms later
# from app.forms.auth import LoginForm, RegistrationForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.dashboard'))
    
    # form = LoginForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(email=form.email.data.lower()).first()
    #     if user is not None and user.verify_password(form.password.data):
    #         login_user(user, remember=form.remember_me.data)
    #         next_page = request.args.get('next')
    #         if not next_page or not next_page.startswith('/'):
    #             next_page = url_for('main.dashboard')
    #         return redirect(next_page)
    #     flash('Invalid email or password.', 'danger')
    
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.dashboard'))
    
    # form = RegistrationForm()
    # if form.validate_on_submit():
    #     user = User(
    #         email=form.email.data.lower(),
    #         username=form.username.data,
    #     )
    #     user.set_password(form.password.data)
    #     db.session.add(user)
    #     db.session.commit()
    #     flash('You are now registered! Please log in.', 'success')
    #     return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    """User logout route"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))