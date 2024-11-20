from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Initialize extensions
db = SQLAlchemy()
load_dotenv()

def create_app():
    app = Flask(__name__)

    
    # Load configuration from .env
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # Initialize extensions
    db.init_app(app)

    # Import and register Blueprints
    from app.routes.routes import main
    app.register_blueprint(main)

    return app
