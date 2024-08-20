from app import app, db  # Import the app and db from your main Flask application

with app.app_context():
    db.create_all()
