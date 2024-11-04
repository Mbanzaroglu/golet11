from backend import create_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from backend.mysql_connector import initialize_database

app = create_app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

# Uygulama başlatıldığında veritabanını başlat
print("Initializing database...")
initialize_database()  # Tabloları oluşturacak

if __name__ == '__main__':
    app.run(debug=True)
