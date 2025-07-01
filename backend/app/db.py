# MongoDB connection utility (to be implemented) 

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
DB_NAME = os.getenv('MONGODB_DB', 'webhook_db')

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

def get_events_collection():
    return db['events'] 