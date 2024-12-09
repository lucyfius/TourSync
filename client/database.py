from pymongo import MongoClient
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# MongoDB configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
MONGODB_DB = os.getenv('MONGODB_DB', 'toursync')

class MongoSchema:
    TOURS_COLLECTION = {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'required': ['property_id', 'tour_time', 'end_time', 'client_name', 'phone_number'],
                'properties': {
                    'property_id': {'bsonType': 'string'},
                    'tour_time': {'bsonType': 'date'},
                    'end_time': {'bsonType': 'date'},
                    'status': {'enum': ['scheduled', 'completed', 'cancelled', 'no_show']},
                    'client_name': {'bsonType': 'string'},
                    'phone_number': {'bsonType': 'string'},
                    'created_at': {'bsonType': 'date'},
                    'updated_at': {'bsonType': 'date'}
                }
            }
        }
    }

def get_database():
    try:
        client = MongoClient(MONGODB_URI)
        db = client[MONGODB_DB]
        return db
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {e}")
        raise

def init_mongodb():
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    
    try:
        # Create collections with validation
        db.create_collection('tours', **MongoSchema.TOURS_COLLECTION)
        db.create_collection('properties')
        
        # Create indexes
        db.tours.create_index([('tour_time', 1)])
        db.tours.create_index([('property_id', 1), ('status', 1)])
        db.properties.create_index([('address', 1)], unique=True)
        
        logging.info("MongoDB initialized successfully")
    except Exception as e:
        logging.warning(f"Collection initialization warning: {e}")