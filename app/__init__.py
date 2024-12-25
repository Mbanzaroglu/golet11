from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os
from flask_login import LoginManager
from dotenv import load_dotenv  # dotenv kütüphanesi eklendi
from app.models.models import User
from app.utils.db_connection import get_db_connection_and_cursor

# .env dosyasını yükle
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Load configuration from .env
    app.secret_key = os.getenv('SECRET_KEY')  # .env dosyasından SECRET_KEY alınıyor
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Veritabanı bağlantısı
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.permanent_session_lifetime = timedelta(minutes=int(os.getenv('SESSION_LIFETIME', 30)))  # Varsayılan 30 dk

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'  # Giriş sayfası rotası

    @login_manager.user_loader
    def load_user(user_id):
        try:
            with get_db_connection_and_cursor() as (conn, cursor):
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                user_data = cursor.fetchone()
        except Exception as e:
            print('Veritabanı hatası:', e)
            user_data = None
        if user_data:
            return User(user_data)
        else:
            return None

    # Blueprint'lerinizi kaydedin
    from app.routes.routes import main_bp
    from app.routes.auth import auth_bp
    from app.routes.favorites import fav_bp
    from app.routes.track import track_bp
    from app.routes.artist import artist_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(fav_bp, url_prefix='/favorites')
    app.register_blueprint(track_bp, url_prefix='/track') 
    app.register_blueprint(artist_bp,url_prefix='/artist')

    return app
