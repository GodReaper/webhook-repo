import os
from pymongo import MongoClient
from dotenv import load_dotenv
from .logging_config import get_logger

load_dotenv()

logger = get_logger('database')

MONGODB_URI = os.getenv('MONGODB_URI')
DB_NAME = os.getenv('MONGODB_DB', 'webhook_db')

logger.info(f"Initializing database connection to: {DB_NAME}")

try:
    client = MongoClient(MONGODB_URI)
    # Test the connection
    client.admin.command('ping')
    logger.info("Successfully connected to MongoDB")
    
    db = client[DB_NAME]
    logger.info(f"Using database: {DB_NAME}")
    
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    raise

def get_events_collection():
    """Get the events collection with logging"""
    logger.debug("Accessing events collection")
    return db['events']