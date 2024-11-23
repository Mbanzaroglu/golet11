from flask import Blueprint, render_template, session

# Define a Blueprint for routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    # session.permanent = "True" # Set session to permanent (30 minutes)
    return render_template('home.html', title="Home Page")
