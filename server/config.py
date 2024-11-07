import os
import secrets
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Generate a secure default secret key if none is provided
DEFAULT_SECRET_KEY = secrets.token_urlsafe(32)

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///database/tours.db')

# Flask configuration
SECRET_KEY = os.getenv('FLASK_SECRET_KEY', DEFAULT_SECRET_KEY)
DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

def validate_config():
    """Validate and warn about configuration"""
    if os.getenv('FLASK_SECRET_KEY') is None:
        print("WARNING: Using default SECRET_KEY. This is insecure in production.")
        print("Please set FLASK_SECRET_KEY environment variable.")

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SECRET_KEY = SECRET_KEY
    CORS_HEADERS = 'Content-Type'
    RATELIMIT_HEADERS_ENABLED = True
    
    # Security headers
    SECURE_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block',
    }

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    PREFERRED_URL_SCHEME = 'https'
