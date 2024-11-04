from app import create_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.mysql_connector import initialize_database

app = create_app()

# Uygulama başlatıldığında veritabanını başlat
print("Initializing database...")
initialize_database()  # Tabloları oluşturacak

if __name__ == '__main__':
    app.run(debug=True)
