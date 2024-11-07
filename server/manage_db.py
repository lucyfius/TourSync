from flask import Flask
from flask_migrate import Migrate, init as flask_init, migrate as flask_migrate, upgrade as flask_upgrade
from database import app, db
from models import Tour, TourStatus
import os

# Initialize migration directory if it doesn't exist
MIGRATION_DIR = os.path.join(os.path.dirname(__file__), 'migrations')

def init_db():
    """Initialize the database"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

def init_migrations():
    """Initialize migrations directory"""
    with app.app_context():
        migrate = Migrate(app, db)
        if not os.path.exists(MIGRATION_DIR):
            flask_init(directory=MIGRATION_DIR)
            print("Migrations directory created.")
        else:
            print("Migrations directory already exists.")

def create_migration():
    """Create a new migration"""
    with app.app_context():
        migrate = Migrate(app, db)
        flask_migrate(directory=MIGRATION_DIR)
        print("Migration created successfully!")

def upgrade_database():
    """Apply all pending migrations"""
    with app.app_context():
        migrate = Migrate(app, db)
        flask_upgrade(directory=MIGRATION_DIR)
        print("Database upgraded successfully!")

if __name__ == "__main__":
    import sys
    
    commands = {
        "init": init_migrations,
        "migrate": create_migration,
        "upgrade": upgrade_database,
        "init-db": init_db
    }
    
    if len(sys.argv) > 1 and sys.argv[1] in commands:
        commands[sys.argv[1]]()
    else:
        print("Available commands:")
        print("python manage_db.py init     - Initialize migrations directory")
        print("python manage_db.py migrate  - Create new migration")
        print("python manage_db.py upgrade  - Apply migrations")
        print("python manage_db.py init-db  - Initialize database tables") 