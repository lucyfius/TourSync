import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///database/tours.db')

# Flask configuration
SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

# Validate required environment variables
def validate_config():
    required_vars = ['FLASK_SECRET_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )
