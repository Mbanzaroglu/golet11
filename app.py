from app import create_app
from app.utils.mysql_connector import initialize_database
from flask import Flask, render_template

app = create_app()


@app.route('/')
def home():
    return render_template('home.html')

print("Initializing database...")
initialize_database()  # Tabloları oluşturacak

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
