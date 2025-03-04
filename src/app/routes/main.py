from flask import Blueprint, render_template, redirect, url_for

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
def dashboard():
    """Main dashboard for authenticated users"""
    return render_template('dashboard.html')