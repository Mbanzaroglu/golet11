from app import create_app  # Import the factory function from app/__init__.py
from app.utils.mysql_connector import initialize_database
import os

# Create the Flask app using the factory function
app = create_app()


initialize_database()

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
