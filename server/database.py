from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Create absolute path for database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'tours.db')
DATABASE_URL = f'sqlite:///{DB_PATH}'

# Ensure database directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Configure SQLAlchemy with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 5,
    'pool_timeout': 30,
    'pool_recycle': 1800,
    'max_overflow': 10
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Add error handling for database connections
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()