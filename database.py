from pymongo import MongoClient
import logging

logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self):
        self.db = None

    def __getitem__(self, name):
        if self.db is None:
            raise RuntimeError("Database not initialized. Call init_db(app) first.")
        return self.db[name]

    def list_collection_names(self):
        if self.db is None:
            raise RuntimeError("Database not initialized.")
        return self.db.list_collection_names()

db = MongoDB()

def init_db(app):
    """Initialize MongoDB with the Flask app configuration."""
    try:
        client = MongoClient(app.config['MONGO_URI'])
        db_name = app.config['MONGO_URI'].split('/')[-1].split('?')[0]
        if not db_name:
            db_name = 'resume_analyzer_db'
        
        db.db = client[db_name]
        logger.info(f"Successfully connected to MongoDB database: {db_name}")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise e
