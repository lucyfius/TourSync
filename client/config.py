import os
from dotenv import load_dotenv
import logging
from pymongo import MongoClient
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError

# Load environment variables
load_dotenv()

# Application constants
APP_NAME = "TourSync"
DEV_MODE = os.getenv('DEV_MODE', 'True').lower() == 'true'

# MongoDB Atlas configuration
MONGODB_URI = os.getenv('MONGODB_URI')
MONGODB_DB = os.getenv('MONGODB_DB', 'toursync')

# Business rules
BUSINESS_HOURS = {
    'start': 9,  # 9 AM
    'end': 17    # 5 PM
}

WORKING_DAYS = [0, 1, 2, 3, 4]  # Monday (0) through Friday (4)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def get_database():
    """Get MongoDB database connection"""
    try:
        client = MongoClient(MONGODB_URI)
        return client[MONGODB_DB]
    except (ConfigurationError, ServerSelectionTimeoutError) as e:
        logging.error(f"Failed to connect to MongoDB Atlas: {e}")
        raise

def validate_config():
    """Validate and warn about configuration"""
    if not MONGODB_URI:
        raise ValueError(
            "Missing MongoDB Atlas connection string. "
            "Please set MONGODB_URI in your .env file."
        )

    try:
        # Test database connection
        db = get_database()
        db.command('ping')
        logging.info("Successfully connected to MongoDB Atlas")
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB Atlas: {e}")
        if not DEV_MODE:
            raise
        else:
            logging.warning("Running in dev mode - continuing without MongoDB")