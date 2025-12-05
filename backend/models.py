"""
Database models for MongoDB using PyMongo
"""
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from datetime import datetime
from bson import ObjectId
import os

class Database:
    def __init__(self, uri):
        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            # Extract database name from URI or use default
            db_name = uri.split('/')[-1].split('?')[0] if '/' in uri.split('//')[-1] else 'crowd_density_db'
            if not db_name or db_name == uri:
                db_name = 'crowd_density_db'
            self.db = self.client[db_name]
            # Test connection
            self.client.admin.command('ping')
            print(f"[OK] Connected to MongoDB: {db_name}")
            self._init_indexes()
        except Exception as e:
            print(f"[ERROR] MongoDB connection error: {e}")
            print("Please ensure MongoDB is running or check your MONGODB_URI")
            raise
    
    def _init_indexes(self):
        """Initialize database indexes"""
        # User collection indexes
        self.db.users.create_index("email", unique=True)
        # Camera collection indexes
        self.db.cameras.create_index("name", unique=True)
        # DensityLog collection indexes
        self.db.density_logs.create_index([("camera_id", 1), ("timestamp", -1)])
        self.db.density_logs.create_index("timestamp")

db = None

def init_db(uri):
    """Initialize database connection"""
    global db
    db = Database(uri)
    return db

class User:
    @staticmethod
    def create(email, password_hash, name):
        """Create a new user"""
        try:
            if db is None:
                raise Exception("Database not initialized. Please check MongoDB connection.")
            result = db.db.users.insert_one({
                'email': email.lower(),
                'password_hash': password_hash,
                'name': name,
                'created_at': datetime.utcnow()
            })
            return str(result.inserted_id)
        except DuplicateKeyError:
            return None
        except Exception as e:
            print(f"Error creating user: {e}")
            raise
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        try:
            if db is None:
                raise Exception("Database not initialized. Please check MongoDB connection.")
            return db.db.users.find_one({'email': email.lower()})
        except Exception as e:
            print(f"Error finding user by email: {e}")
            return None
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        try:
            return db.db.users.find_one({'_id': ObjectId(user_id)})
        except:
            return None

class Camera:
    @staticmethod
    def create(name, url, location, owner_id):
        """Create a new camera"""
        try:
            result = db.db.cameras.insert_one({
                'name': name,
                'url': url,
                'location': location,
                'owner_id': ObjectId(owner_id),
                'created_at': datetime.utcnow()
            })
            return str(result.inserted_id)
        except DuplicateKeyError:
            return None
    
    @staticmethod
    def find_all():
        """Find all cameras"""
        return list(db.db.cameras.find())
    
    @staticmethod
    def find_by_id(camera_id):
        """Find camera by ID"""
        try:
            return db.db.cameras.find_one({'_id': ObjectId(camera_id)})
        except:
            return None
    
    @staticmethod
    def find_by_owner(owner_id):
        """Find cameras by owner"""
        try:
            return list(db.db.cameras.find({'owner_id': ObjectId(owner_id)}))
        except:
            return []
    
    @staticmethod
    def update(camera_id, updates):
        """Update camera"""
        try:
            result = db.db.cameras.update_one(
                {'_id': ObjectId(camera_id)},
                {'$set': updates}
            )
            return result.modified_count > 0
        except:
            return False
    
    @staticmethod
    def delete(camera_id):
        """Delete camera"""
        try:
            result = db.db.cameras.delete_one({'_id': ObjectId(camera_id)})
            return result.deleted_count > 0
        except:
            return False

class DensityLog:
    @staticmethod
    def create(camera_id, person_count, density_value, alert_triggered=False):
        """Create a new density log entry"""
        try:
            result = db.db.density_logs.insert_one({
                'camera_id': ObjectId(camera_id),
                'timestamp': datetime.utcnow(),
                'person_count': person_count,
                'density_value': density_value,
                'alert_triggered': alert_triggered
            })
            return str(result.inserted_id)
        except:
            return None
    
    @staticmethod
    def find_by_camera(camera_id, limit=100):
        """Find density logs for a camera"""
        try:
            return list(db.db.density_logs.find(
                {'camera_id': ObjectId(camera_id)}
            ).sort('timestamp', -1).limit(limit))
        except:
            return []
    
    @staticmethod
    def find_recent_by_camera(camera_id, minutes=60):
        """Find recent density logs for a camera"""
        from datetime import timedelta
        try:
            cutoff = datetime.utcnow() - timedelta(minutes=minutes)
            return list(db.db.density_logs.find({
                'camera_id': ObjectId(camera_id),
                'timestamp': {'$gte': cutoff}
            }).sort('timestamp', 1))
        except:
            return []

