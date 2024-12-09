from pymongo import MongoClient
import logging
from .config import MONGODB_URI, MONGODB_DB

def init_mongodb():
    """Initialize MongoDB connection"""
    try:
        client = MongoClient(MONGODB_URI)
        db = client[MONGODB_DB]
        # Test the connection
        db.command('ping')
        logging.info("MongoDB Atlas connection successful")
        return db
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB Atlas: {e}")
        raise

def get_database():
    """Get MongoDB database instance"""
    client = MongoClient(MONGODB_URI)
    return client[MONGODB_DB]