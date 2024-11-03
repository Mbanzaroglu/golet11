from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Blueprint ile rotaları import et
    from .routes import main
    app.register_blueprint(main)

    # MySQL veritabanı bağlantısını yapılandır
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # İzleme modunu kapatarak performansı artırır

    # SQLAlchemy'yi uygulama ile başlat
    db.init_app(app)

    return app
