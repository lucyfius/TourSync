import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000/api')

def validate_config():
    required_vars = ['API_BASE_URL']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}\n"
            f"Please check your .env file or environment variables."
        ) 