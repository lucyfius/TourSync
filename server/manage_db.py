from flask import Flask
from flask.cli import FlaskGroup
from database import app, db
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

def migrate_db():
    with app.app_context():
        # Generate migration
        from flask_migrate import Migrate, migrate
        migrate = Migrate(app, db)
        migrate()
        print("Migration completed successfully!")

def upgrade_db():
    with app.app_context():
        # Apply migrations
        from flask_migrate import Migrate, upgrade
        migrate = Migrate(app, db)
        upgrade()
        print("Database upgraded successfully!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "init":
            init_db()
        elif sys.argv[1] == "reset":
            reset_db()
        elif sys.argv[1] == "migrate":
            migrate_db()
        elif sys.argv[1] == "upgrade":
            upgrade_db()
    else:
        print("Available commands:")
        print("python manage_db.py init    - Initialize the database")
        print("python manage_db.py reset   - Reset the database")
        print("python manage_db.py migrate - Generate migrations")
        print("python manage_db.py upgrade - Apply migrations") 