from app import create_app  # Import the factory function from app/__init__.py

# Create the Flask app using the factory function
app = create_app()

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
