from flask import Blueprint, render_template

# Define a Blueprint for routes
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html', title="Home Page")
