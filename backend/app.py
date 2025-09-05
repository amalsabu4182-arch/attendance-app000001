from flask import Flask
from flask_cors import CORS
from datetime import datetime, timedelta

# Change 1: Use absolute imports instead of relative imports
from models import db, User
from routes import bp as api_blueprint

def create_app():
    app = Flask(__name__)
    CORS(app) # Enable CORS for all routes

    # --- Database Configuration ---
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your_very_secret_key' # Change this in production

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(api_blueprint, url_prefix='/api')

    with app.app_context():
        db.create_all()
        # Create a default admin user if one doesn't exist
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', role='admin')
            admin.set_password('adminpass')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created.")

    return app

if __name__ == '__main__':
    app = create_app()
    # Change: Run on port 5001 to avoid conflicts with other applications
    app.run(debug=True, port=5001)

