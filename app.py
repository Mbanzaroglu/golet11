from app import create_app
from app.utils.mysql_connector import initialize_database
from flask import Flask, render_template

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
