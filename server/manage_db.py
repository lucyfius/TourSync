from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models after db initialization
from models import Tour, TourStatus

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")

def reset_db():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        # Create all tables
        db.create_all()
        print("Database reset successfully!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "init":
            init_db()
        elif sys.argv[1] == "reset":
            reset_db()
        elif sys.argv[1] == "migrate":
            # Migrations are handled by flask-migrate CLI
            print("Please use 'flask db migrate' for migrations")
    else:
        print("Available commands:")
        print("python manage_db.py init  - Initialize the database")
        print("python manage_db.py reset - Reset the database")
        print("flask db migrate         - Generate migrations")
        print("flask db upgrade         - Apply migrations") 