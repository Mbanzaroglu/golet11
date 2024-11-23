from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.routes.routes import main_bp
from datetime import timedelta
import os

# Initialize extensions
# db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Load configuration from .env
    app.secret_key = os.getenv('SECRET_KEY') # Set secret key for session management
    app.permanent_session_lifetime = timedelta(minutes=30) # Set session lifetime to 30 minutes
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # # Initialize extensions
    # db.init_app(app)

    #register Blueprints
    app.register_blueprint(main_bp)

    return app
